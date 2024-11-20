import xml.etree.ElementTree as ET

def extract_routes_from_vehicles(input_file, output_routes_file, output_vehicles_file):
    # XML 파일 파싱
    tree = ET.parse(input_file)
    root = tree.getroot()
    
    routes = ET.Element("routes")
    vehicles = ET.Element("vehicles")
    
    route_counter = 1  # route의 ID를 위한 카운터
    
    # vehicle 요소를 반복하면서 route 정보를 추출
    for vehicle in root.findall('vehicle'):
        # vehicle에서 route 정보 가져오기
        route_edges = vehicle.find('route').text.strip() if vehicle.find('route') is not None else ""
        
        # route가 없다면 스킵
        if not route_edges:
            continue
        
        # 새로운 route ID를 생성
        route_id = f"route_{route_counter}"
        route_counter += 1
        
        # route 엘리먼트 생성
        route_element = ET.SubElement(routes, "route", id=route_id)
        route_element.text = route_edges
        
        # vehicle의 route를 route_id로 업데이트
        vehicle.set("route", route_id)
        
        # vehicle을 새로운 vehicles 리스트에 추가
        vehicles.append(vehicle)
    
    # 새로운 routes XML 파일 생성
    route_tree = ET.ElementTree(routes)
    route_tree.write(output_routes_file, encoding="UTF-8", xml_declaration=True)

    # 새로운 vehicles XML 파일 생성
    vehicles_tree = ET.ElementTree(vehicles)
    vehicles_tree.write(output_vehicles_file, encoding="UTF-8", xml_declaration=True)

# 호출 예시
extract_routes_from_vehicles("hack.routes.xml", "hackid.routes.xml", "hackid.vehicles.xml")

