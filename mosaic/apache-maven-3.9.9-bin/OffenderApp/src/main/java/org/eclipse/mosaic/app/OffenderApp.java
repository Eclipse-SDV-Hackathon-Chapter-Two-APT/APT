package org.eclipse.mosaic.app;

import org.eclipse.mosaic.fed.application.app.AbstractApplication;
import org.eclipse.mosaic.fed.application.app.api.VehicleApplication;
import org.eclipse.mosaic.fed.application.app.api.os.VehicleOperatingSystem;
import org.eclipse.mosaic.lib.objects.vehicle.VehicleData;
import org.eclipse.mosaic.lib.util.scheduling.Event;
import org.eclipse.mosaic.rti.TIME;

import javax.annotation.Nonnull;
import javax.annotation.Nullable;

public class OffenderApp extends AbstractApplication<VehicleOperatingSystem> implements VehicleApplication {

    private static final float ESCAPE_SPEED = 25 / 3.6f;
    private boolean escaping = false;

    @Override
    public void onStartup() {
//        System.out.println("가해 차량이 도로에 진입했습니다.");
    }

    @Override
    public void onVehicleUpdated(@Nullable VehicleData previousVehicleData, @Nonnull VehicleData updatedVehicleData) {
        if (escaping) {
//            System.out.println("가해 차량이 도주 중입니다.");
        }
    }

    public void onCollision() {
//        System.out.println("가해 차량이 충돌 후 도주를 시작합니다.");
        startEvading();
    }

    public void startEvading() {
        if (!escaping) {
            getOs().changeSpeedWithInterval(ESCAPE_SPEED, 5 * TIME.SECOND);
            escaping = true;
//            System.out.println("가해 차량 도주 속도 설정: " + (ESCAPE_SPEED * 3.6f) + " km/h");
        }
    }

    public void stopEvading() {
        if (escaping) {
            getOs().resetSpeed();
            escaping = false;
//            System.out.println("가해 차량이 도주를 멈췄습니다.");
        }
    }

    @Override
    public void processEvent(Event event) {
    }

    @Override
    public void onShutdown() {
//        System.out.println("가해 차량 시스템 종료");
    }
}
