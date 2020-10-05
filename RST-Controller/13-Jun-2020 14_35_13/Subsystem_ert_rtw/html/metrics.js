function CodeMetrics() {
	 this.metricsArray = {};
	 this.metricsArray.var = new Array();
	 this.metricsArray.fcn = new Array();
	 this.metricsArray.var["rtDW"] = {file: "C:\\Users\\AK47\\IdeaProjects\\RST Controller\\13-Jun-2020 14_35_13\\Subsystem_ert_rtw\\Subsystem.c",
	size: 48};
	 this.metricsArray.var["rtM_"] = {file: "C:\\Users\\AK47\\IdeaProjects\\RST Controller\\13-Jun-2020 14_35_13\\Subsystem_ert_rtw\\Subsystem.c",
	size: 4};
	 this.metricsArray.var["rtU"] = {file: "C:\\Users\\AK47\\IdeaProjects\\RST Controller\\13-Jun-2020 14_35_13\\Subsystem_ert_rtw\\Subsystem.c",
	size: 16};
	 this.metricsArray.var["rtY"] = {file: "C:\\Users\\AK47\\IdeaProjects\\RST Controller\\13-Jun-2020 14_35_13\\Subsystem_ert_rtw\\Subsystem.c",
	size: 8};
	 this.metricsArray.fcn["Subsystem_initialize"] = {file: "C:\\Users\\AK47\\IdeaProjects\\RST Controller\\13-Jun-2020 14_35_13\\Subsystem_ert_rtw\\Subsystem.c",
	stack: 0,
	stackTotal: 0};
	 this.metricsArray.fcn["Subsystem_step"] = {file: "C:\\Users\\AK47\\IdeaProjects\\RST Controller\\13-Jun-2020 14_35_13\\Subsystem_ert_rtw\\Subsystem.c",
	stack: 8,
	stackTotal: 8};
	 this.getMetrics = function(token) { 
		 var data;
		 data = this.metricsArray.var[token];
		 if (!data) {
			 data = this.metricsArray.fcn[token];
			 if (data) data.type = "fcn";
		 } else { 
			 data.type = "var";
		 }
	 return data; }; 
	 this.codeMetricsSummary = '<a href="Subsystem_metrics.html">Global Memory: 76(bytes) Maximum Stack: 8(bytes)</a>';
	}
CodeMetrics.instance = new CodeMetrics();
