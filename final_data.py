from dependencies import *

print('Loading Final DataFrame')

# files: list[str] = glob('data/final/*.csv')

# if (len(files) == 0):
# 	path: Path = Path(glob('data/final/*.csv.gz')[-1])
# else:
# 	path: Path = Path(files[-1])

# day: date = datetime.strptime(str(path).split('\\')[-1].split('.')[0], '%Y-%m-%d').date()

path = glob('data/final/*.pkl')[0]

start = datetime.now()
# final_df:pd.DataFrame = pd.read_csv(path, low_memory=False)
final_df:pd.DataFrame = pd.read_pickle(path)
end = datetime.now()

print(f'Loaded in {(end - start).seconds} Seconds')
