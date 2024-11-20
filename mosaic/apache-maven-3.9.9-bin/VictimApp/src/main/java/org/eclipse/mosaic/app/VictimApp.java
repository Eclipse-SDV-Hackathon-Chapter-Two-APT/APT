package org.eclipse.mosaic.app;

import org.eclipse.mosaic.fed.application.ambassador.simulation.communication.CellModule;
import org.eclipse.mosaic.fed.application.app.AbstractApplication;
import org.eclipse.mosaic.fed.application.app.api.VehicleApplication;
import org.eclipse.mosaic.fed.application.app.api.os.VehicleOperatingSystem;
import org.eclipse.mosaic.lib.objects.vehicle.VehicleData;
import org.eclipse.mosaic.lib.util.scheduling.Event;
import org.eclipse.mosaic.lib.geo.*;
import org.eclipse.mosaic.lib.objects.v2x.*;
import org.eclipse.mosaic.fed.cell.module.*;
import org.eclipse.mosaic.lib.objects.addressing.AdHocMessageRoutingBuilder;
//import org.eclipse.mosaic.lib.objects.addressing.AdHocChannel;
import org.eclipse.mosaic.fed.application.ambassador.simulation.communication.*;

public class VictimApp extends AbstractApplication<VehicleOperatingSystem> implements VehicleApplication {  

    private boolean collisionDetected = false;
    private static final float COLLISION_SPEED_THRESHOLD = 5.0f;

    @Override
    public void onStartup() {
//        System.out.println("피해 차량 대기 중...");
    }

    private void sendAccidentSignal() {
        GeoPoint accidentLocation = getOperatingSystem().getVehicleData().getPosition();
        GeoCircle transmissionArea = new GeoCircle(accidentLocation, 3000); 

        String hostName = getOperatingSystem().getVehicleData().getRouteId(); 
        GeoPoint sourcePosition = accidentLocation;

        AdHocMessageRoutingBuilder routingBuilder = new AdHocMessageRoutingBuilder(hostName, sourcePosition);
        MessageRouting routing = routingBuilder.geoCast(transmissionArea, null);

//        MessageRouting routing = routingBuilder.unicast("ServerId");
        
        String accidentMessageContent = "Accident detected at position: " + accidentLocation;
        long messageSize = accidentMessageContent.getBytes().length;

        V2xMessage accidentMessage = new GenericV2xMessage(routing, "AccidentAlert", messageSize);

        getOperatingSystem().getCellModule().sendV2xMessage(accidentMessage);

//        System.out.println("충돌 감지: 경찰 차량에 사고 메시지 전송 (Geocast)");
    }

    @Override
    public void processEvent(Event event) {
        if (collisionDetected) {
//            System.out.println("피해 차량이 충돌을 감지했습니다!");
            sendAccidentSignal(); 
            collisionDetected = false; 
        }
    }

    @Override
    public void onVehicleUpdated(VehicleData previousVehicleData, VehicleData updatedVehicleData) {
        float previousSpeed = (float) previousVehicleData.getSpeed();
        float currentSpeed = (float) updatedVehicleData.getSpeed();

        if (!collisionDetected && Math.abs(currentSpeed - previousSpeed) > COLLISION_SPEED_THRESHOLD) {
//            System.out.println("비정상적인 속도 변화 감지! 충돌 가능성 있음.");
            collisionDetected = true;
            processEvent(new Event(getOperatingSystem().getSimulationTime(), this));
        }
    }

    @Override
    public void onShutdown() {
//        System.out.println("피해 차량 시스템 종료");
    }
}
