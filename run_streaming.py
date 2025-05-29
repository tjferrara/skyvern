import asyncio
import subprocess
import os

import structlog
import typer

from skyvern.forge import app
from skyvern.forge.sdk.api.files import get_skyvern_temp_dir

INTERVAL = 1
LOG = structlog.get_logger()


async def run() -> None:
    # Create temp directory structure for organizations
    temp_dir = get_skyvern_temp_dir()
    
    while True:
        # run subprocess to take screenshot
        base_screenshot_path = f"{temp_dir}/skyvern_screenshot.png"
        subprocess.run(
            f"xwd -root | xwdtopnm 2>/dev/null | pnmtopng > {base_screenshot_path}", shell=True, env={"DISPLAY": ":99"}
        )

        # Check if screenshot was created successfully
        if not os.path.exists(base_screenshot_path):
            LOG.debug("Failed to create screenshot")
            await asyncio.sleep(INTERVAL)
            continue

        # Get all organizations and save streaming files for each
        try:
            # Get all organizations from database
            organizations = await app.DATABASE.get_all_organizations()
            
            for org in organizations:
                org_id = org.organization_id
                
                # Create organization directory if it doesn't exist
                org_dir = f"{temp_dir}/{org_id}"
                os.makedirs(org_dir, exist_ok=True)
                
                # Copy screenshot to organization directory
                org_screenshot_path = f"{org_dir}/skyvern_screenshot.png"
                subprocess.run(f"cp {base_screenshot_path} {org_screenshot_path}", shell=True)
                
                # Save general screenshot for organization to S3
                try:
                    await app.STORAGE.save_streaming_file(org_id, "skyvern_screenshot.png")
                    LOG.debug("Saved general screenshot to S3", org_id=org_id)
                except Exception as e:
                    LOG.debug("Failed to save general screenshot to S3", org_id=org_id, error=str(e))
                
                # Try to get active workflow runs and save specific screenshots
                try:
                    from skyvern.forge.sdk.workflow.models.workflow import WorkflowRunStatus
                    active_workflows = await app.DATABASE.get_workflow_runs(
                        organization_id=org_id,
                        status=[WorkflowRunStatus.running]
                    )
                    
                    for workflow_run in active_workflows:
                        workflow_file = f"{org_dir}/{workflow_run.workflow_run_id}.png"
                        subprocess.run(f"cp {base_screenshot_path} {workflow_file}", shell=True)
                        
                        # Save to S3 for this specific workflow
                        try:
                            await app.STORAGE.save_streaming_file(org_id, f"{workflow_run.workflow_run_id}.png")
                            LOG.debug("Saved workflow screenshot to S3", workflow_run_id=workflow_run.workflow_run_id, org_id=org_id)
                        except Exception as e:
                            LOG.debug("Failed to save workflow screenshot to S3", workflow_run_id=workflow_run.workflow_run_id, error=str(e))
                
                except Exception as e:
                    LOG.debug("Failed to get active workflows", org_id=org_id, error=str(e))
                    
        except Exception as e:
            LOG.error("Failed to process streaming screenshots", error=str(e))

        await asyncio.sleep(INTERVAL)


if __name__ == "__main__":
    typer.run(asyncio.run(run()))
