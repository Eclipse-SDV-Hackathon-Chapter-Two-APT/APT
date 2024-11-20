package org.eclipse.mosaic.app;

import org.eclipse.mosaic.fed.application.app.AbstractApplication;
import org.eclipse.mosaic.fed.application.app.api.CommunicationApplication;
import org.eclipse.mosaic.fed.application.app.api.os.ServerOperatingSystem;
import org.eclipse.mosaic.fed.application.ambassador.simulation.communication.ReceivedAcknowledgement;
import org.eclipse.mosaic.fed.application.ambassador.simulation.communication.ReceivedV2xMessage;
import org.eclipse.mosaic.lib.geo.GeoCircle;
import org.eclipse.mosaic.lib.geo.GeoPoint;
import org.eclipse.mosaic.lib.objects.v2x.V2xMessage;
import org.eclipse.mosaic.lib.objects.v2x.EncodedPayload;

public class AccidentServerApp extends AbstractApplication<ServerOperatingSystem> implements CommunicationApplication {

    @Override
    public void onStartup() {
        getLog().infoSimTime(this, "AccidentServerApp initialized and ready to process accident signals...");
        getOs().getCellModule().enable();
    }

    @Override
    public void onMessageReceived(ReceivedV2xMessage receivedV2xMessage) {
        final V2xMessage message = receivedV2xMessage.getMessage();

        getLog().infoSimTime(this, "Received message from vehicle: {}",
                message.getRouting().getSource().getSourceName());

        // Assuming the message body contains some data that can indicate the message type
        if (isAccidentAlert(message)) {
            GeoPoint accidentLocation = GeoPoint.latLon(52.5200, 13.4050);

            double radiusInMeters = 50.0;
            GeoCircle accidentArea = new GeoCircle(accidentLocation, radiusInMeters);

            getLog().infoSimTime(this, "Accident alert received! Location: {}, Radius: {}m",
                    accidentLocation, radiusInMeters);

            handleAccident(accidentArea);
        } else {
            getLog().infoSimTime(this, "Ignoring non-accident message.");
        }
    }

    /*
     * @param message V2xMessage
     * @return true if the message indicates an accident alert
     */
    private boolean isAccidentAlert(V2xMessage message) {
        if (message.getPayload() != null) {
            String payloadString = decodePayloadToString(message.getPayload());
            
            // Check if the decoded string contains the keyword "accident"
            return payloadString != null && payloadString.contains("accident");
        }
        return false;
    }

    private String decodePayloadToString(EncodedPayload payload) {
        try {
            // Check if the payload has a byte array
            byte[] byteData = payload.getBytes();
            
            // If the byte array exists, convert it to a string using UTF-8 encoding
            if (byteData != null) {
                return new String(byteData, "UTF-8");
            }
        } catch (Exception e) {
            return null;
        }
        return null; 
    }



    /*
     * @param accidentArea 사고 발생 영역 (GeoCircle)
     */
    private void handleAccident(GeoCircle accidentArea) {
        System.out.println("Accident area: Center=Lat " + accidentArea.getCenter().getLatitude() +
                ", Lon " + accidentArea.getCenter().getLongitude() +
                ", Radius=" + accidentArea.getRadius() + "m");
    }

    @Override
    public void onAcknowledgementReceived(ReceivedAcknowledgement acknowledgement) {
        
    }

    @Override
    public void onCamBuilding(org.eclipse.mosaic.fed.application.ambassador.simulation.communication.CamBuilder camBuilder) {
        
    }

    @Override
    public void onMessageTransmitted(org.eclipse.mosaic.interactions.communication.V2xMessageTransmission v2xMessageTransmission) {
        
    }

    @Override
    public void processEvent(org.eclipse.mosaic.lib.util.scheduling.Event event) {
        
    }

    @Override
    public void onShutdown() {
        getLog().infoSimTime(this, "AccidentServerApp shutting down...");
    }
}
