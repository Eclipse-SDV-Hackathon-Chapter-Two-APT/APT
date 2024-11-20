@ECHO OFF
SetLocal EnableDelayedExpansion

set libs=

set Filter= .\tools\scenario-convert-*.jar
for %%f in (%Filter%) do (
if not "!libs!" == "" set libs=!libs!;
    set libs=!libs!%%f
)

java -cp !libs!;lib\mosaic\*;lib\extended\*;lib\third-party\* com.dcaiti.mosaic.tools.scenarioconvert.core.Starter %*

EndLocal

exit /b %errorlevel%
