
    var locations = [
      { lat: 37.5665, lng: 126.9780, name: "서울", description: "한국의 수도" },
      { lat: 37.433746, lng: 127.029681, name: "국립과천과학관천문대", description: "경기 과천시 상하벌로 110" },
      { lat: 36.383518, lng: 127.356858, name: "국립중앙과학관 천체관측소", description: "대전 유성구 구성동 5" },
      { lat: 35.852131, lng: 128.463651, name: "국립대구과학관 천문대", description: "대구 달성군 유가읍 테크노대로6길 20" }
    ];

    function initMap() {
      var mapOptions = {
        center: { lat: 36.5, lng: 127.5 },
        zoom: 7
      };

      var map = new google.maps.Map(document.getElementById("map"), mapOptions);

      locations.forEach(function(location) {
        var marker = new google.maps.Marker({
          position: { lat: location.lat, lng: location.lng },
          map: map,
          title: location.name
        });

        var infoWindow = new google.maps.InfoWindow({
          content: "<h3>" + location.name + "</h3><p>" + location.description + "</p>"
        });

        marker.addListener("click", function() {
          infoWindow.open(map, marker);
        });
      });
    }