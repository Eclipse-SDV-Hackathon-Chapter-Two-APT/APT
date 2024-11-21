# APT

## Project Overview

Nowadays, we are exposed to various dangers on the road regardless of place or time. For example, a collision between vehicles in a city center can cause serious traffic disruption, and bad weather creates the worst possible situation for inattentive drivers. These traffic problems can have negative effects not only on the people involved, but also on other drivers.
Therefore, we would like to propose a service that can protect surrounding vehicles from potential threats. We also propose a comprehensive traffic accident prevention system that guides the police to respond quickly to accidents and prevent secondary damage.

### Use case

- hit & run

	In the event of a collision between vehicles, there are cases where the offending vehicle flees the scene. Drivers who flee can cause traffic chaos with their hasty driving, and the scope of police response varies depending on the time of reporting. Hit-and-run accidents accounted for 24% of the 7,454 crashes reported by NHTSA in 2020.

- heay rainny

	Bad weather poses a serious threat to drivers. Heavy rain, heavy snow, fog, etc. can impair visibility and function, and accidents caused by these can have more serious consequences than normal conditions. NHTSA reported that over a 10-year period, 10 percent of all crashes occurred on days when it rained.

## Description
### Architecture
### Features

Surrounding vehicles judge the traffic situation based on the information of the dangerous vehicle they received. Based on the judged information, they immediately display appropriate warning notifications on the HUD so that the driver can respond to potential threats in advance.

**Dangerous Car**
	Publishes VSS messages (crash information, speed, engine speed, humidity, etc.). This information is collected in real time and serves as the basis for situational assessment.

**Car dirver**
- Example 1 - Hit & Run
1) Notify the surroundings that an accident has occurred.
2) Provide the distance to the accident site so that the driver can prepare for congested situations.
3) Provide the recommended speed according to the driving speed so that the driver can prepare for sudden situations.

- Example 2 - Inclement weather (heavy rain)
1) Provide guidance to use fog lights for safe driving.
2) Provide guidance to maintain an appropriate speed.
3) Provide traffic signs for safe driving such as no overtaking.

**Police**
	Receive vehicle data sets including the locations of vehicles reporting dangerous situations to identify dangerous areas and their causes. Provide additional information (route to the point) appropriate to the given information.

 ### Simulation
 ### Potential Improvement
