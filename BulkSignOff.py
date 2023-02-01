def BULK_SIGN_OFF_COUNTER(DF_SIGNATURES, setting, sign_threshold):
    
    '''
    
    Check for instances of bulk sign offs and save these results in a Dataframe. 
    
    Within this dataframe, list the name of the indivDocument IDual commiting a bulk sign off, the date & time of the bulk sign off,
    as well as the number of documents signed off simultaneously.
    
    Input:
    -------
    
    DF_SIGNATURES [pd.DataFrame]: Dataframe containing all the document signatures.
    
    setting [char]: 's' or 'm' or 'h' or 'd', refering to: 'second', 'minute', 'hour' or 'day' respectively. This specifies
    if we're checking for bulk sign offs within the same second/minute/hour/day.
    
    sign_threshold [int]: Number specifying what counts as a bulk sign off. If the number of sings > sign_threshold. 
    List as a bulk sign off.
    
    Output:
    -------
    
    DF [pd.DataFrame]: Dataframe listing all instances of bulk sign offs. (To be displayed)
    
    '''

    # List of all people signing the documents
    participants = DF_SIGNATURES['Name'].unique()

    # Initialise dataframe to store results in
    details = details = {'Name': [], 'Bulk Sign Off Time': [], 'Number of Signatures': []}
    DF = pd.DataFrame(details)

    # For every participant
    # -----------------------------------------------------

    for j in range(len(participants)):

        # Create a temporary dataframe for this participant and his/her signatures.
        temp_DF = DF_SIGNATURES[ DF_SIGNATURES['Name'] == participants[j] ]

        # Extract date and times of his/her signatures
        # -----------------------------------------------------

        # Total number of documents in engagement
        n_docs = len(temp_DF)

        date_time = temp_DF['SignDate']
        date_time = np.array(temp_DF['SignDate'], dtype = str)

        if setting == 's':
            date_time = [x[0:19] for x in date_time]

        if setting == 'm':
            # Date and Time (by minutes)
            date_time = [x[0:16] for x in date_time]

        if setting == 'h':
            # Date and Time (by hour)
            date_time = [x[0:13] for x in date_time]

        if setting == 'd':
            # Date and Time (by day)
            date_time = [x[0:10] for x in date_time]

        # ==============================================
        # Count signatures
        # ==============================================

        # Unique signature instances (unique time instances)
        instances = np.array(np.unique(date_time, return_counts=True))[0]
        sign_time = [0] * len(instances)
        counts = [0] * len(instances)


        # For every unique instance a signature took place
        # --------------------------------------------------

        for k in range(len(instances)):

            # Lambda function to check if the date/time (according to the relevant setting) matches the instance.
            mask = lambda test: test.apply(str).str.replace(".","", regex = True).str.contains(instances[k] , na=False, flags=re.IGNORECASE)
            
            # Temporary dataframe listing all signatures associated with this time instance
            temp_DF2 = temp_DF[mask(temp_DF['SignDate'])]
            sign_time[k] = instances[k]

            # Count the number of UNIQUE documents signed on this instance of time.
            counts[k] = len(temp_DF2['Document ID'].unique())

            # ==============================================
            # Count Bulk Sign Off Instances
            # ==============================================

            # If (for this instance of time), more UNIQUE documents than the <sign_threshold> has been signed. 

            if counts[k] > sign_threshold:

                # Store information in a dataframe
                details = {'Name': [participants[j]], 'Bulk Sign Off Time': [sign_time[k]], 
                           'Number of Signatures': [counts[k]]}

                RESULT = pd.DataFrame(details)

                # Append results
                DF = pd.concat([DF, RESULT], axis=0)
                
    
    # Display results
    DF = DF.reset_index(drop = True)
    display(DF)

    return None



'''
Generate some random data.
'''


details = {'Name': [], 'Document ID': [], 'SignDate': []}
DUMMY_DF = pd.DataFrame(details)

# Generate random timestamps between: Current Time - 1 Hour and Current Time + 1 Hour
start_date = datetime.datetime.now() - timedelta(hours=1)
end_date = start_date + timedelta(hours=1)

# Generate a list of 5 random names
participants = [names.get_full_name(), names.get_full_name(), names.get_full_name(), names.get_full_name(), names.get_full_name()]

# Generate 5000 random data entries into the dummy dataframe
for i in range(5000):
    
    random_name = random.choice(participants)
    
    random_date = start_date + (end_date - start_date) * random.random()
    
    random_date = str(random_date)
    
    DUMMY_DF.loc[len(DUMMY_DF.index)] = [random_name, i, random_date] 
    
    
'''
Test Bulk Sign Off Counter on the random data.
'''

BULK_SIGN_OFF_COUNTER(DUMMY_DF, 's', 2) # Bulk Sign Offs (> 2 documents) in the same hour.
BULK_SIGN_OFF_COUNTER(DUMMY_DF, 'm', 10) # Bulk Sign Offs (> 10 documents) in the same minute.
BULK_SIGN_OFF_COUNTER(DUMMY_DF, 'h', 20) # Bulk Sign Offs (> 20 documents) in the same hour.
BULK_SIGN_OFF_COUNTER(DUMMY_DF, 'd', 50) # Bulk Sign Offs (> 50 documents) in the same day.