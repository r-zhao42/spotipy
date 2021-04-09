from dbscan_nd import DBSCAN_Algo, load_data, initialize_data

data = initialize_data(load_data('FooBar_No_Labels.csv'))

run_0 = DBSCAN_Algo(data=data, epsilon=0.085, min_points=25)
run_0.run()
c0 = run_0.clusters[2]
print(c0)

new_data = run_0.clusters[0].points + run_0.clusters[1].points
run_1 = DBSCAN_Algo(new_data, epsilon=0.075, min_points=25)
run_1.run()
run_1.print_summary()
run_1.draw_with_matplotlib()
