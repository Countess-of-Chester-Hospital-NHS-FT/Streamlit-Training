
import simpy
import pandas as pd
from sim_tools.distributions import (Exponential, Lognormal)
from scipy.stats import sem, t
from vidigi.utils import VidigiPriorityStore, populate_store # animation package

class g: # global
    patient_inter_visit = 10
    number_of_receptionists = 1
    mean_reception_time = 2
    sd_reception_time = 0.5
    number_of_drs = 1
    mean_dr_time = 10
    sd_dr_time = 2
    sim_duration = 720 # clinic open for 12 hours
    number_of_runs = 100

class Patient:
    def __init__(self, p_id):
        self.id = p_id
        self.priority = 0

class Model:
    def __init__(self, run_number):
        self.env = simpy.Environment()
        self.event_log = [] 
        self.patient_counter = 0
        self.run_number = run_number
        self.init_resources()

        # Initialise distributions for generators
        self.patient_inter_visit_dist = Exponential(mean = g.patient_inter_visit, random_seed = self.run_number*1)
        self.mean_reception_time_dist = Lognormal(g.mean_reception_time, g.sd_reception_time, random_seed = self.run_number*2)
        self.mean_dr_time_dist = Lognormal(g.mean_dr_time, g.sd_dr_time, random_seed = self.run_number*3)

    def init_resources(self):
        self.receptionists = VidigiPriorityStore(self.env)
        populate_store(num_resources=g.number_of_receptionists,
                       simpy_store=self.receptionists,
                       sim_env=self.env)
        self.drs = VidigiPriorityStore(self.env)
        populate_store(num_resources=g.number_of_drs,
                       simpy_store=self.drs,
                       sim_env=self.env)
    
    def generator_patient_arrivals(self):
        while True:
            self.patient_counter += 1
            p = Patient(self.patient_counter) # creates the patient

            self.env.process(self.attend_ed(p)) # pushes them through the door

            sampled_inter = self.patient_inter_visit_dist.sample() # time to next patient arriving
            yield self.env.timeout(sampled_inter)
    
    def attend_ed(self, patient):
        # arrival and departure events are needed for the animation - even if they are the same as the wait begins.
        self.event_log.append(
            {'patient' : patient.id,
             'priority' : patient.priority,
             'event_type' : 'arrival_departure',
             'event' : 'arrival',
             'time' : self.env.now}
        )
        
        # Start waiting for receptionist
        self.event_log.append(
            {'patient' : patient.id,
             'priority' : patient.priority,
             'event_type' : 'queue',
             'event' : 'reception_wait_begins',
             'time' : self.env.now}
        )

        receptionist_resource = yield self.receptionists.get(priority=patient.priority)
        # Get a receptionist
        self.event_log.append(
            {'patient' : patient.id,
            'priority' : patient.priority,
            'event_type' : 'resource_use',
            'event' : 'reception_begins',
            'time' : self.env.now,
            'resource_id' : receptionist_resource.id_attribute
            }
            )
        
        sampled_reception_time = self.mean_reception_time_dist.sample()
        yield self.env.timeout(sampled_reception_time)

        self.event_log.append(
        {'patient' : patient.id,
        'priority' : patient.priority,
        'event_type' : 'resource_use_end',
        'event' : 'reception_complete',
        'time' : self.env.now,
        'resource_id' : receptionist_resource.id_attribute
        }
        )

        self.receptionists.put(receptionist_resource) # put the receptionist back
        # Finished with receptionist & start waiting for Dr

        self.event_log.append(
            {'patient' : patient.id,
             'priority' : patient.priority,
             'event_type' : 'queue',
             'event' : 'dr_wait_begins',
             'time' : self.env.now}
        )

        dr_resource = yield self.drs.get(priority=patient.priority)
        # Get a Dr
        self.event_log.append(
            {'patient' : patient.id,
            'priority' : patient.priority,
            'event_type' : 'resource_use',
            'event' : 'dr_begins',
            'time' : self.env.now,
            'resource_id' : dr_resource.id_attribute
            }
            )
        
        sampled_dr_time = self.mean_dr_time_dist.sample()
        yield self.env.timeout(sampled_dr_time)

        self.event_log.append(
        {'patient' : patient.id,
        'priority' : patient.priority,
        'event_type' : 'resource_use_end',
        'event' : 'dr_complete',
        'time' : self.env.now,
        'resource_id' : dr_resource.id_attribute
        }
        )

        self.drs.put(dr_resource) # put the Dr back
        # Finished with Dr

        self.event_log.append(
        {'patient' : patient.id,
        'priority' : patient.priority,
        'event_type' : 'arrival_departure',
        'event' : 'depart',
        'time' : self.env.now}
        )

    def run(self):
        self.env.process(self.generator_patient_arrivals()) # kicks off the generators
        self.env.run(until=g.sim_duration)
        self.event_log = pd.DataFrame(self.event_log)
        self.event_log["run"] = self.run_number
        return {'event_log':self.event_log}

class Trial:
    def  __init__(self):
        self.all_event_logs = []
        self.patient_df = pd.DataFrame()
        self.run_summary_df = pd.DataFrame()
        self.trial_summary_df = pd.DataFrame()

    def run_trial(self):
        for run in range(g.number_of_runs):
            my_model = Model(run) # creates a model instance
            model_outputs = my_model.run() # runs the model instance
            event_log = model_outputs["event_log"] 
            self.all_event_logs.append(event_log)
        self.all_event_logs = pd.concat(self.all_event_logs) # squishes the list of lists of dictionaries into a dataframe
        self.wrangle_data()
        self.summarise_runs()
        self.summarise_trial()
        return self.all_event_logs, self.patient_df, self.run_summary_df, self.trial_summary_df
    
    def wrangle_data(self):
        df = self.all_event_logs[["patient", "event", "time", "run", "priority"]]
        df = df.pivot(index=["patient","run", "priority"], columns="event", values="time")
        df = (df.reset_index()
                .rename_axis(None,axis=1))
        df["q_time_reception"] = df["reception_begins"] - df["reception_wait_begins"]
        #df["q_time_hrs"] = df["q_time"] / 60.0
        df["q_time_dr"] = df["dr_begins"] - df["dr_wait_begins"]
        self.patient_df = df

    def summarise_runs(self):
        run_summary = self.patient_df
        # note that q_time is na where a patient is not admitted so is automatically omitted from summary calcs
        run_summary = run_summary.groupby("run").agg(
            total_demand=("patient", "count"),
            reception_mean_qtime=("q_time_reception", "mean"),
            reception_std_qtime=("q_time_reception", "std"),
            reception_min_qtime=("q_time_reception", "min"),
            reception_max_qtime=("q_time_reception", "max"),
            dr_mean_qtime=("q_time_dr", "mean"),
            dr_std_qtime=("q_time_dr", "std"),
            dr_min_qtime=("q_time_dr", "min"),
            dr_max_qtime=("q_time_dr", "max"),
        )
        self.run_summary_df = run_summary

    def summarise_trial(self):
        trial_summary = self.run_summary_df
        trial_summary = trial_summary.transpose()
        newdf = pd.DataFrame(index=trial_summary.index)
        newdf.index.name = "Metric"
        newdf["Mean"] = trial_summary.mean(axis=1)
        newdf["St. dev"] = trial_summary.std(axis=1)
        newdf['St. error'] = sem(trial_summary, axis=1, nan_policy='omit')
        # Confidence intervals (95%) - t distribution method accounts for sample size
        confidence = 0.95
        h = newdf['St. error'] * t.ppf((1 + confidence) / 2, g.number_of_runs - 1)
        newdf['Lower 95% CI'] = newdf['Mean'] - h
        newdf['Upper 95% CI'] = newdf['Mean'] + h
        newdf['Min'] = trial_summary.min(axis=1)
        newdf['Max'] = trial_summary.max(axis=1)
        newdf=newdf.round(2)
        self.trial_summary_df = newdf
    

# Normally keep this commented out - uncomment to do a quick check of model results
# my_trial = Trial()
# print(f"Running {g.number_of_runs} simulations......")
# all_event_logs, patient_df, run_summary_df, trial_summary_df =  my_trial.run_trial()
#display(my_trial.all_event_logs.head(1000))
#display(my_trial.patient_df.head(1000))
#display(my_trial.patient_df_nowarmup.head(1000))
#display(my_trial.run_summary_df)
#display(my_trial.trial_summary_df)