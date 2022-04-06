from cx_Freeze import * 
import sys
includefiles=['icon.ico','attach.png','browse.png','clear.png','email.png','exit.png','mail.png',
              'mic.png']
base=None
if sys.platform=="win32":
    base="Win32GUI"

shortcut_table=[
    ("DesktopShortcut",
     "DesktopFolder",
     "Emai Sender",
     "TARGETDIR",
     "[TARGETDIR]\email_sender.exe",
     None,
     None,
     None,
     None,
     None,
     None,
     "TARGETDIR",
     )
]
msi_data={"Shortcut":shortcut_table}

bdist_msi_options={'data':msi_data}
setup(
    version="0.1",
    description="Email sender application",
    author="Anuj Bhor",
    name="Email Sender",
    options={'build_exe':{'include_files':includefiles},'bdist_msi':bdist_msi_options,},
    executables=[
        Executable(
            script="email_sender.py",
            base=base,
            icon='icon.ico',
        )
    ]
)
