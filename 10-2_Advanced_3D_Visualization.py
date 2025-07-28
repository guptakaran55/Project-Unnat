#javascript
// Advanced Three.js visualization with real - time updates


class Advanced3DVisualization {
constructor(containerId) {
this.container = document.getElementById(containerId);
this.scene = new THREE.Scene();
this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
this.renderer = new THREE.WebGLRenderer({antialias: true

});

this.setupRenderer();
this.setupLighting();
this.setupControls();
this.setupPostProcessing();

this.buildingMesh = null;
this.environmentMap = null;
this.weatherAnimation = null;
}

setupRenderer()
{
    this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
this.renderer.setClearColor(0x87CEEB); // Sky
blue
this.renderer.shadowMap.enabled = true;
this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
this.container.appendChild(this.renderer.domElement);
}

setupLighting()
{
// Sunlight
simulation
based
on
location and time
this.sunLight = new
THREE.DirectionalLight(0xffffff, 1);
this.sunLight.castShadow = true;
this.sunLight.shadow.mapSize.width = 2048;
this.sunLight.shadow.mapSize.height = 2048;
this.scene.add(this.sunLight);

// Ambient
lighting
const
ambientLight = new
THREE.AmbientLight(0x404040, 0.4);
this.scene.add(ambientLight);

// Sky
dome
this.createSkyDome();
}

createSkyDome()
{
    const
skyGeometry = new
THREE.SphereGeometry(1000, 32, 32);
const
skyMaterial = new
THREE.ShaderMaterial({
    uniforms: {
        topColor: {value: new THREE.Color(0x0077ff)},
        bottomColor: {value: new THREE.Color(0xffffff)},
        offset: {value: 33},
        exponent: {value: 0.6}
    },
    vertexShader: `
    varying vec3 vWorldPosition;
void
main()
{
    vec4
worldPosition = modelMatrix * vec4(position, 1.0);
vWorldPosition = worldPosition.xyz;
gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}
`,
fragmentShader: `
uniform
vec3
topColor;
uniform
vec3
bottomColor;
uniform
float
offset;
uniform
float
exponent;
varying
vec3
vWorldPosition;
void
main()
{
    float
h = normalize(vWorldPosition + offset).y;
gl_FragColor = vec4(mix(bottomColor, topColor, max(pow(max(h, 0.0), exponent), 0.0)), 1.0);
}
`,
side: THREE.BackSide
});

const
sky = new
THREE.Mesh(skyGeometry, skyMaterial);
this.scene.add(sky);
}

createBuildingVisualization(buildingData)
{
// Remove
existing
building
if (this.buildingMesh)
{
    this.scene.remove(this.buildingMesh);
}

// Create
building
geometry
const
buildingGeometry = this.createBuildingGeometry(buildingData);
const
buildingMaterial = this.createBuildingMaterial(buildingData);

this.buildingMesh = new
THREE.Mesh(buildingGeometry, buildingMaterial);
this.buildingMesh.castShadow = true;
this.buildingMesh.receiveShadow = true;
this.scene.add(this.buildingMesh);

// Add
windows
this.addWindows(buildingData);

// Add
environmental
context
this.addEnvironmentalContext(buildingData.location);

// Animate
sun
path
this.animateSunPath(buildingData.location);
}

createBuildingGeometry(buildingData)
{
    const
geometry = new
THREE.BoxGeometry(
    buildingData.length,
    buildingData.height,
    buildingData.width
);

// Apply
building
orientation
geometry.rotateY(THREE.MathUtils.degToRad(buildingData.orientation));

return geometry;
}

addWindows(buildingData)
{
const
windowGeometry = new
THREE.PlaneGeometry(2, 1.5);
const
windowMaterial = new
THREE.MeshPhysicalMaterial({
    color: 0x87CEEB,
    metalness: 0.0,
    roughness: 0.1,
    transmission: 0.9,
    thickness: 0.1
});

// Calculate
window
positions
based
on
WWR
const
numWindows = Math.floor(buildingData.window_wall_ratio * 20);

for (let i = 0; i < numWindows; i++) {
    const window = new THREE.Mesh(windowGeometry, windowMaterial);

// Position windows on building facade
const angle = (i / numWindows) * Math.PI * 2;
const radius = Math.max(buildingData.length, buildingData.width) / 2 + 0.1;

window.position.x = Math.cos(angle) * radius;
window.position.z = Math.sin(angle) * radius;
window.position.y = buildingData.height / 4 + (i % 3) * (buildingData.height / 4);

window.lookAt(0, window.position.y, 0);

this.scene.add(window);
}
}

animateSunPath(location)
{
// Animate
sun
movement
throughout
the
day
const
sunPath = this.calculateSunPath(location.lat, location.lng);

let
currentHour = 6; // Start
at
sunrise

const
animateSun = () = > {
    const
sunPosition = sunPath[Math.floor(currentHour)];

if (sunPosition)
{
    this.sunLight.position.set(
        sunPosition.x * 100,
        sunPosition.y * 100,
        sunPosition.z * 100
    );

// Update
sun
color
based
on
time
of
day
const
sunColor = this.getSunColor(currentHour);
this.sunLight.color.setHex(sunColor);
}

currentHour += 0.1;
if (currentHour > 18)
currentHour = 6; // Reset
to
sunrise

requestAnimationFrame(animateSun);
};

animateSun();
}

addWeatherVisualization(weatherData)
{
// Add
rain, snow, wind
visualization
if (weatherData.precipitation > 0) {
this.addRainEffect(weatherData.precipitation);
}

if (weatherData.wind_speed > 5) {
this.addWindEffect(weatherData.wind_speed, weatherData.wind_direction);
}

if (weatherData.temperature < 0) {
this.addSnowEffect();
}
}

addRainEffect(intensity)
{
const
rainGeometry = new
THREE.BufferGeometry();
const
rainCount = intensity * 1000;
const
rainPositions = new
Float32Array(rainCount * 3);

for (let i = 0; i < rainCount * 3; i += 3) {
    rainPositions[i] = Math.random() * 200 - 100; // x
rainPositions[i + 1] = Math.random() * 200 + 50; // y
rainPositions[i + 2] = Math.random() * 200 - 100; // z
}

rainGeometry.setAttribute('position', new
THREE.BufferAttribute(rainPositions, 3));

const
rainMaterial = new
THREE.PointsMaterial({
    color: 0x4A90E2,
    size: 0.5,
    transparent: true,
    opacity: 0.8
});

const
rain = new
THREE.Points(rainGeometry, rainMaterial);
this.scene.add(rain);

// Animate
rain
falling
const
animateRain = () = > {
    const
positions = rain.geometry.attributes.position.array;

for (let i = 1; i < positions.length; i += 3)
{
    positions[i] -= 2; // Fall
speed

if (positions[i] < 0)
{
    positions[i] = 200; // Reset
to
top
}
}

rain.geometry.attributes.position.needsUpdate = true;
requestAnimationFrame(animateRain);
};

animateRain();
}

render()
{
requestAnimationFrame(() = > this.render());
this.renderer.render(this.scene, this.camera);
}
}