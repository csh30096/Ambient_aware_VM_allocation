#define _CRT_OBSOLETE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>
//CPU utilization is calculated with /proc/stat
long long int total_tick_old = 0.0;
long long int idle_old = 0.0;

double util(int Num){
        FILE *stat_read;
        long long int fields[9][11];
        long long int total_tick;
        long long int idle;
        long long int del_total_tick, del_idle;
        int i = Num + 1, j;
        double percent_usage;
        int retval;
        char buffer[1000];

        stat_read = fopen("/proc/stat", "r");
        if(stat_read == NULL){
                perror("Error");
        }


        for(int k = 0; k < 9; k++){
                retval = fscanf(stat_read, "%s %lld %lld %lld %lld %lld %lld %lld %lld %lld %lld",
                                buffer,
                                &fields[k][0],
                                &fields[k][1],
                                &fields[k][2],
                                &fields[k][3],
                                &fields[k][4],
                                &fields[k][5],
                                &fields[k][6],
                                &fields[k][7],
                                &fields[k][8],
                                &fields[k][9]);
        }

        if(retval < 4)
        {
                perror("Error");
        }


        for(j = 0, total_tick = 0; j < 10; j++){
                        total_tick += fields[i][j];
        }
        idle = fields[i][3];
        del_total_tick = total_tick - total_tick_old;
        del_idle = idle - idle_old;
        total_tick_old = total_tick;
        idle_old = idle;

        percent_usage = ((del_total_tick - del_idle) / (double) del_total_tick);
        if(del_total_tick == 0) percent_usage = 0.0;
        fclose(stat_read);
        return percent_usage;
}

int main(){
	double percent_total_usage;
	double ambient = 0.0;
	// Use your maximum frequency of the CPU
	double max_freq = 4.7;
	double DCC = 0.0;
	double a, b, c;
	FILE *fo, *amb;

	// if your CPUs are not equal to my configuration, it needs to recalculate.
	a = -0.55;
	b = 22.3;
	c = -60.77;

	while (1){
		percent_total_usage = util(-1);
	        fo = fopen("DCC_calculated", "w");
		// Use your Ambient temperature file
	        amb = fopen("/home/server13/Desktop/Ambient_Temperature", "r");
	        fscanf(amb, "%f", &ambient);
		DCC = a * ambient;
		DCC = DCC + (b*max_freq);
		DCC = DCC + (c*percent_total_usage);
		
		fprintf (fo, "%.2f", DCC);
		fclose(amb);
		fclose(fo);
		sleep(1);
	}
	return 0;
}
