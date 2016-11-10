# scc-cdp-api-examples

### This repo contains short example scripts that demonstrate and exmplain aspects of the Smart+Connected Digital Platform APIs.

##Examples

####There are currently three example Python scripts in this repo:

* cdp101\_python\_example.py - **Authentication and API Requests**
	* This sample script demonstrates logging into the Smart+Connected Digital Platform and making an additional request. All Smart+Connected Digital Platform APIs (except authentication) require access tokens. In this example, those access tokens are obtained through the /login API and used to make another API request.

* cdp102\_python\_example.py - **Retrieving Information from the Smart+Connected Digital Platform**
	* This sample script demonstrates making several Smart+Connected Digital Platform. In this example, additional information about the locations available to the current user and about the capabilities of the Smart+Connected Digital Platform instance itself is retrieved.

* cdp103\_python\_example.py - **Requesting Real Time Data from the Smart+Connected Digital Platform**
	* This sample script demonstrates getting Real Time Data from the Smart+Connected Digital Platform.  In this example, real time device information for lighting is retrieved and visualized as a simple pie chart.
