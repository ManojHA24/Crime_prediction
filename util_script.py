import pandas as pd

def create_df(filenames):
    main_df = pd.read_csv(filenames[0])
    print("Finished Loading Chicago Crime Dataset File for the year "+filenames[0][-8:-4]+".")
    main_df = main_df[list(main_df.columns[:22])]
    for file in filenames[1:]:
        print("Finished loading Chicago Crime Dataset file for the year "+file[-8:-4]+".")
        df_temp = pd.read_csv(file)
        df_temp = df_temp[list(df_temp.columns[:22])]
        main_df = main_df.append(df_temp, ignore_index=True)
    print("All data files loaded onto the Main Dataframe.\n\n")
    
    return main_df


