// API 키
var apiKey = "5ab77328109f5e57098ff9c5f111f641";

// 현재 위치의 날씨 정보를 가져오는 함수
function getCurrentWeather() {
  // 위치 정보를 가져오기 위한 Geolocation API 사용
  navigator.geolocation.getCurrentPosition(
    function(position) {
      var latitude = position.coords.latitude;
      var longitude = position.coords.longitude;

      // OpenWeatherMap API 엔드포인트 URL
      var apiUrl = "https://api.openweathermap.org/data/2.5/weather?lat=" + latitude + "&lon=" + longitude + "&appid=" + apiKey;

      // API 요청 보내기
      fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
          // 날씨 정보에서 필요한 데이터 추출
          var cityName = data.name;
          var weatherDescription = data.weather[0].description;
          var temperature = data.main.temp;

          var celsius = temperature - 273.15;

          // 결과값을 HTML에 업데이트
          document.getElementById("city").textContent = cityName;
          document.getElementById("weather").textContent = weatherDescription;
          document.getElementById("temperature").textContent = celsius.toFixed(1) + "°C";

          // 이미지와 관측상태 업데이트
          updateWeatherInfo(weatherDescription);
        })
        .catch(error => {
          console.log("API 요청 중 오류가 발생했습니다.", error);
        });
    },
    function(error) {
      console.log("위치 정보를 가져올 수 없습니다.", error);
    }
  );
}

// 날씨에 따라 이미지와 관측상태 업데이트
function updateWeatherInfo(weatherDescription) {
  var lowerCaseDescription = weatherDescription.toLowerCase();
  var imageSrc = "";
  var weatherStatus = "";

  if (lowerCaseDescription.includes("clear") || lowerCaseDescription.includes("sunny")) {
    imageSrc = "static/img/clear.png"; // 맑은 날씨 이미지 파일 경로
    weatherStatus = "하늘이 깨끗해 잘 보일겁니다.";
  } else if (
    lowerCaseDescription.includes("cloud") ||
    lowerCaseDescription.includes("overcast") ||
    lowerCaseDescription.includes("fog") ||
    lowerCaseDescription.includes("haze")
  ) {
    imageSrc = "static/img/cloudy.png"; // 흐린 날씨 이미지 파일 경로
    weatherStatus = "날이 좋지 않아 관측에 어려움이 있을겁니다.";
  } else if (
    lowerCaseDescription.includes("mist") ||
    lowerCaseDescription.includes("rain")
  ) {
    imageSrc = "static/img/mist.png"; // 비오는 날씨 이미지 파일 경로
    weatherStatus = "날이 좋지 않아 관측에 어려움이 있을겁니다.";
  } else if (
    lowerCaseDescription.includes("snow")
  ) {
    imageSrc = "static/img/snow.png"; // 눈오는 날씨 이미지 파일 경로
    weatherStatus = "날이 좋지 않아 관측에 어려움이 있을겁니다.";
  }else {
    imageSrc = "static/img/default.png"; // 기본 이미지 파일 경로
    weatherStatus = "날이 좋지 않아 관측에 어려움이 있을겁니다.";
  }

  // 이미지와 관측상태 업데이트
  var imgElement = document.getElementById("weather-image").getElementsByTagName("img")[0];
  imgElement.src = imageSrc;
  document.getElementById("weather-status").textContent = weatherStatus;
}

// 페이지 로드 시 날씨 정보 가져오는 함수 호출
window.onload = getCurrentWeather;
