try:
    import database
    print("Import successful")
    print(dir(database))
except Exception as e:
    import traceback
    traceback.print_exc()
