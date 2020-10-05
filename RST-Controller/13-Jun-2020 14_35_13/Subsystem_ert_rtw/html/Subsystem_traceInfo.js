function RTW_rtwnameSIDMap() {
	this.rtwnameHashMap = new Array();
	this.sidHashMap = new Array();
	this.rtwnameHashMap["<Root>"] = {sid: "Subsystem"};
	this.sidHashMap["Subsystem"] = {rtwname: "<Root>"};
	this.rtwnameHashMap["<S1>"] = {sid: "rst:8"};
	this.sidHashMap["rst:8"] = {rtwname: "<S1>"};
	this.rtwnameHashMap["<S1>/In1"] = {sid: "rst:9"};
	this.sidHashMap["rst:9"] = {rtwname: "<S1>/In1"};
	this.rtwnameHashMap["<S1>/In2"] = {sid: "rst:10"};
	this.sidHashMap["rst:10"] = {rtwname: "<S1>/In2"};
	this.rtwnameHashMap["<S1>/1//S(z)"] = {sid: "rst:5"};
	this.sidHashMap["rst:5"] = {rtwname: "<S1>/1//S(z)"};
	this.rtwnameHashMap["<S1>/R(z)"] = {sid: "rst:7"};
	this.sidHashMap["rst:7"] = {rtwname: "<S1>/R(z)"};
	this.rtwnameHashMap["<S1>/Sum1"] = {sid: "rst:4"};
	this.sidHashMap["rst:4"] = {rtwname: "<S1>/Sum1"};
	this.rtwnameHashMap["<S1>/T(z)"] = {sid: "rst:3"};
	this.sidHashMap["rst:3"] = {rtwname: "<S1>/T(z)"};
	this.rtwnameHashMap["<S1>/Out1"] = {sid: "rst:11"};
	this.sidHashMap["rst:11"] = {rtwname: "<S1>/Out1"};
	this.getSID = function(rtwname) { return this.rtwnameHashMap[rtwname];}
	this.getRtwname = function(sid) { return this.sidHashMap[sid];}
}
RTW_rtwnameSIDMap.instance = new RTW_rtwnameSIDMap();
