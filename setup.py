from cx_Freeze import setup, Executable


setup(
    name="Recommender",
    version="0.1",
    description="Music Recommender App",
    executables=[Executable("Recommender.py")],
    options={
        'build_exe': {
            'packages': ['pandas', 'sklearn'],
            'include_files': ['allkpopsongsfordataset.csv', 'allsongsfordataset.csv'],
        }
    }
)