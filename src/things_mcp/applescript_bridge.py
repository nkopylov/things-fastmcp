import subprocess
import logging
from typing import Optional, List, Union

logger = logging.getLogger(__name__)


def run_applescript(script: str) -> str:
    """Run an AppleScript and return the result as a string."""
    try:
        result = subprocess.run(
            ["osascript", "-e", script], capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logger.error(f"AppleScript error: {e.stderr}")
        return ""


def add_todo_direct(
    title: str,
    notes: Optional[str] = None,
    when: Optional[str] = None,
    tags: Optional[Union[str, List[str]]] = None,
) -> str:
    """Add a new todo to Things using AppleScript and return its ID."""
    # Convert tags list to comma-separated string if it's a list
    if isinstance(tags, list):
        tags = ", ".join(tags)

    # Build the AppleScript
    script = (
        """
    tell application "Things3"
        set newToDo to make new to do with properties {name:"%s"}
    """
        % title
    )

    # Add optional properties
    if notes:
        script += """
        set notes of newToDo to "%s"
        """ % notes.replace('"', '\\"')

    if when:
        script += (
            """
        set activation date of newToDo to date "%s"
        """
            % when
        )

    if tags:
        script += """
        set tagList to {}
        """

        # Handle comma-separated list of tags
        if isinstance(tags, str):
            tags_list = [t.strip() for t in tags.split(",")]
            for tag in tags_list:
                if tag:
                    script += """
                    -- Ensure tag exists
                    set tagExists to false
                    repeat with t in tags
                        if name of t is "%s" then
                            set tagExists to true
                            set end of tagList to t
                            exit repeat
                        end if
                    end repeat
                    
                    if not tagExists then
                        set newTag to make new tag with properties {name:"%s"}
                        set end of tagList to newTag
                    end if
                    """ % (tag, tag)

            script += """
            set tag of newToDo to tagList
            """

    # Complete the script and get the ID
    script += """
        return id of newToDo
    end tell
    """

    # Execute the AppleScript
    try:
        result = run_applescript(script)
        logger.info(f"Created todo with title: {title}, ID: {result}")
        return result
    except Exception as e:
        logger.error(f"Failed to create todo: {e}")
        return ""


def update_todo_direct(
    id: str,
    title: Optional[str] = None,
    notes: Optional[str] = None,
    when: Optional[str] = None,
    deadline: Optional[str] = None,
    tags: Optional[Union[str, List[str]]] = None,
    completed: Optional[bool] = None,
    canceled: Optional[bool] = None,
) -> bool:
    """Update a todo in Things using AppleScript."""
    # Convert tags list to comma-separated string if it's a list
    if isinstance(tags, list):
        tags = ", ".join(tags)

    # Build the AppleScript
    script = (
        """
    tell application "Things3"
        try
            set theToDo to to do id "%s"
    """
        % id
    )

    # Add updates for each property
    if title is not None:
        script += """
            set name of theToDo to "%s"
        """ % title.replace('"', '\\"')

    if notes is not None:
        script += """
            set notes of theToDo to "%s"
        """ % notes.replace('"', '\\"')

    if when is not None:
        if when == "":
            script += """
            set activation date of theToDo to missing value
            """
        else:
            script += (
                """
            set activation date of theToDo to date "%s"
            """
                % when
            )

    if deadline is not None:
        if deadline == "":
            script += """
            set deadline of theToDo to missing value
            """
        else:
            script += (
                """
            set deadline of theToDo to date "%s"
            """
                % deadline
            )

    if tags is not None:
        script += """
        set tagList to {}
        """

        # Handle comma-separated list of tags
        if isinstance(tags, str):
            tags_list = [t.strip() for t in tags.split(",")]
            for tag in tags_list:
                if tag:
                    script += """
                    -- Ensure tag exists
                    set tagExists to false
                    repeat with t in tags
                        if name of t is "%s" then
                            set tagExists to true
                            set end of tagList to t
                            exit repeat
                        end if
                    end repeat
                    
                    if not tagExists then
                        set newTag to make new tag with properties {name:"%s"}
                        set end of tagList to newTag
                    end if
                    """ % (tag, tag)

            script += """
            set tag of theToDo to tagList
            """

    if completed is not None:
        if completed:
            script += """
            set status of theToDo to completed
            """
        else:
            script += """
            set status of theToDo to open
            """

    if canceled is not None:
        if canceled:
            script += """
            set status of theToDo to canceled
            """
        else:
            script += """
            set status of theToDo to open
            """

    # Complete the script
    script += """
            return id of theToDo
        on error errMsg
            log "Error updating todo: " & errMsg
            return ""
        end try
    end tell
    """

    # Execute the AppleScript
    try:
        result = run_applescript(script)
        if result:
            logger.info(f"Updated todo with ID: {id}")
            return True
        else:
            logger.error(f"Failed to update todo with ID: {id}")
            return False
    except Exception as e:
        logger.error(f"Failed to update todo: {e}")
        return False
