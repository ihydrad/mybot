from jobParser import JobParser


str = JobParser("sterlitamak")

data = str.get_from_web()

print(data)

