import numpy as np

from datafeed.mining.gplearn.genetic import SymbolicRegressor

funcs = [make_function(**func._asdict()) for func in generic_funcs]

instruments = 'csi300'
seed = 4
reseed_everything(seed)

cache = {}
#device = torch.device('cuda:0')



features = ['open_', 'close', 'high', 'low', 'volume', 'vwap']
constants = [f'Constant({v})' for v in [-30., -10., -5., -2., -1., -0.5, -0.01, 0.01, 0.5, 1., 2., 5., 10., 30.]]
terminals = features + constants

X_train = np.array([terminals])
y_train = np.array([[1]])

est_gp = SymbolicRegressor(population_size=1000,
                           generations=40,
                           init_depth=(2, 6),
                           tournament_size=600,
                           stopping_criteria=1.,
                           p_crossover=0.3,
                           p_subtree_mutation=0.1,
                           p_hoist_mutation=0.01,
                           p_point_mutation=0.1,
                           p_point_replace=0.6,
                           max_samples=0.9,
                           verbose=1,
                           parsimony_coefficient=0.,
                           random_state=seed,
                           function_set=funcs,
                           metric=Metric,
                           const_range=None,
                           n_jobs=1
                           )
est_gp.fit(X_train, y_train, callback=ev)
print(est_gp._program.execute(X_train))
