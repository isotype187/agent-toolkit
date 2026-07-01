import os
import subprocess


class ProjectContext:

    def __init__(self):

        self.root = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                ".."
            )
        )


    def git_status(self):

        try:
            result = subprocess.run(
                ["git", "status", "--short"],
                cwd=self.root,
                capture_output=True,
                text=True
            )

            return result.stdout.strip()

        except Exception as e:
            return f"Git error: {e}"


    def files(self):

        output = []

        for root, dirs, files in os.walk(self.root):

            for file in files:

                path = os.path.join(
                    root,
                    file
                )

                output.append(
                    os.path.relpath(
                        path,
                        self.root
                    )
                )

        return output


    def info(self):

        return {
            "project_root": self.root,
            "git_status": self.git_status(),
            "file_count": len(self.files())
        }


context = ProjectContext()
