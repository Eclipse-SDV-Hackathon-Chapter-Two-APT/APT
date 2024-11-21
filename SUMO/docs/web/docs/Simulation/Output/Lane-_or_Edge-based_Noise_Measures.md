---
title: Lane- or Edge-based Noise Measures
---

The edge/lane based noise output based on Harmonoise writes information
about the noise produced on edges/lanes. The model was generated within
the EC-project [Imagine](https://web.archive.org/web/20220901035449/http://www.imagine-project.org/). Its
description can be found in the deliverable 18 of this project ([D18 The
Harmonoise Engineering
model](https://web.archive.org/web/20220901035449/http://www.imagine-project.org/bestanden/D18_WP3_HAR32TR-040922-DGMR20.pdf)).

!!! missing
    Add a model description here

!!! note
    Please be aware that adding up noise is not as easy as calculating other emissions or consumption values because the perceived sound of two cars is not the sum of the volumes of the individual cars since the decibel scale itself is logarithmic.

## Instantiating within the Simulation

### Edge-Based Noise Output

An edge-based noise emissions output is defined way within an additional
file as following:

```xml
<edgeData id="<DETECTOR_ID>" type="harmonoise" period="<PERIOD>" file="<OUTPUT_FILE>" [excludeEmpty="true"]/>
```

### Lane-Based Noise Output

An edge-based noise emissions output is defined way within an additional
file as following:

```xml
<laneData id="<DETECTOR_ID>" type="harmonoise" period="<PERIOD>" file="<OUTPUT_FILE>" [excludeEmpty="true"]/>
```

### Attributes, for both Edge- and Lane-Based Noise Output

| Attribute Name | Value Type  | Description          |
| -------------- | ----------- | --------------------------------------------- |
| **id**         | id (string) | The id of the detector       |
| **file**       | filename    | The path to the output file. The path may be relative.     |
| period (alias freq) | int (time)  | The aggregation period the values the detector collects shall be summed up. If not given, the whole time range between begin and end is aggregated |
| begin          | int (time)  | The time to start writing (intervals starting before this time are discarded). If not given, the simulation's begin is used.  |
| end            | int (time)  | The time to end writing (intervals starting at or after this time are discarded). If not given the simulation's end is used.   |
| excludeEmpty   | bool        | If set, edges/lanes which were not used by a vehicle during this period will not be written; *default: false*.   |

## Generated Output

### Edge-Based Network States

### Lane-Based Network States

### Value Descriptions

| Name           | Type                 | Description                              |
| -------------- | -------------------- | ---------------------------------------- |
| begin          | (simulation) seconds | The first time step the values were collected in            |
| end            | (simulation) seconds | The last time step + DELTA_T in which the reported values were collected    |
| edge\@id        | (edge) id            | The name of the reported edge        |
| lane\@id        | (lane) id            | The name of the reported lane         |
| sampledSeconds | s                    | Number seconds vehicles were measured on the edge/lane (may be subseconds if a vehicle enters/leaves the edge/lane) |
| noise          | dBA                  | The average noise generated by the vehicles on the edge/lane during the interval |

## Notes

Notes:

- Per default, all edges are written, even those on which no vehicle
  drove. It can be disabled setting the
  `excludeEmpty` attribute to true.
- The interval end is the interval begin + aggregation time, meaning
  that values were collected within these steps excluding the end time
  itself. If the simulation ends before the last interval is over, the
  interval will be pruned.
- The output file will be generated, does not have to exist earlier
  and will be overwritten if existing without any warning. The folder
  the output file shall be generated in must exist.
- If you need only information about the network states during certain
  time periods, you may constraint generation of the dumps by giving
  attributes "`begin="<TIME>\[,<TIME>\]+"`"
  and "`end="<TIME>\[,<TIME>\]+"`". When at
  least one combination is given, dumps will be written only if an
  according begin/end-pair exists for the current time. This means,
  only those intervals will be saved for which
  begin\[x\]<=INTERVAL_END and end\[x\]\>=INTERVAL_BEGIN. All dumps
  will cover the complete simulation if no values for begin/end are
  given.

## See Also

- [edge/lane-based network performance measures
  output](../../Simulation/Output/Lane-_or_Edge-based_Traffic_Measures.md)
  and [edge/lane-based vehicular pollutant emission
  output](../../Simulation/Output/Lane-_or_Edge-based_Emissions_Measures.md)
  which have similar formats
- The
  [mpl_dump_onNet.py](../../Tools/Visualization.md#mpl_dump_onnetpy)
  script can display values of this output as a colored net (and
  further [visualization tools](../../Tools/Visualization.md) exist).