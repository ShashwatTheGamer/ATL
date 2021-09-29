var planet = getLevel();

var path, spaceShip, cash, diamonds, jwellery, sword, end;
var pathImg, spaceShipImg, cashImg, endImg;
var treasureCollection = 0;
var cashG, swordGroup;
var playButton, playButtonImg, replayButton, replayButtonImg, nextButtonImg;
var asteroid1, asteroid2, asteroid3, asteroid4, asteroid5;

var heartindicatorImg, coinsindicatorImg;

var levelup0Img, levelup1Img, levelup2Img, levelup3Img;
var levelup;

var lives = 3;
var level = 0;

var SPEED = 10;
var gameState = "PLAY";

var path = "https://"+window.location.hostname+"/";

var scrollSpeed = 2;


function preload() {

	background1Img = loadImage(path+"images/background4.png");
	background2Img = loadImage(path+"images/Background10.png");

	asteroid1 = loadImage(path+"images/parts/part1.png");
	asteroid2 = loadImage(path+"images/parts/part2.png");
	asteroid3 = loadImage(path+"images/parts/part3.png");
	asteroid4 = loadImage(path+"images/parts/part4.png");
	asteroid5 = loadImage(path+"images/parts/part5.png");

	gameoverImg = loadImage(path+"images/gameover1.png");

	spaceShipImg = loadImage(path+"images/spaceship.png");
	endImg = loadAnimation(path+"images/gameOver.png");
	startButtonImg = loadImage(path+"images/buttons/start.png");
	resetButtonImg = loadImage(path+"images/buttons/next.png");

	pauseButtonImg = loadImage(path+"images/icons/pause.png");

	playButtonImg = loadImage(path+"images/icons/play.png");

	logoImg = loadImage(path+"images/logo.png");

	progressAnim = loadAnimation(path+"images/progress/progress 0.png", path+"images/progress/progress 60.png", path+"images/progress/progress 100.png");

	levelup0Img = loadImage(path+"images/level up/level up 0.png");
	levelup1Img = loadImage(path+"images/level up/level up 1.png");
	levelup2Img = loadImage(path+"images/level up/level up 2.png");
	levelup3Img = loadImage(path+"images/level up/level up 3.png");

	coinsImg = loadImage(path+"images/coin.png");
	coins2Img = loadImage(path+"images/coin2.png");
	gemsImg = loadImage(path+"images/gems.png");

	nextButtonImg = loadImage(path+"images/buttons/next.png");

}

function setup() {

	createCanvas(windowWidth, windowHeight);

	logo = createSprite(windowWidth / 2, windowHeight / 3);
	logo.addImage(logoImg);
	logo.visible = false;

	levelup = createSprite((windowWidth / 2), (windowHeight / 2));
	levelup.visible = false;

	startButton = createSprite((windowWidth / 2) + 50, (windowHeight / 2) + 150);
	startButton.addImage(startButtonImg);
	startButton.scale = 0.7;

	pauseButton = createSprite(windowWidth-100, 100, 10, 10);
	pauseButton.addImage(pauseButtonImg);
	pauseButton.visible = false;

	playButton = createSprite(windowWidth/2, windowHeight/2, 10, 10);
	playButton.addImage(playButtonImg);
	playButton.visible = false;

	nextButton = createSprite((windowWidth / 2) + 50, (windowHeight / 2) + 150);
	nextButton.addImage(nextButtonImg);
	nextButton.scale = 0.7;
	nextButton.visible = false;

	resetButton = createSprite(windowWidth/2, (windowHeight/2)+100);
	resetButton.addImage(resetButtonImg);
	resetButton.visible = false;

	coincount = createSprite((windowWidth / 2) - 45, windowHeight / 15);
	coincount.addImage(coins2Img);
	coincount.visible = false;

	x2 = width;
	x1 = 0;

	cashG = new Group();
	asteroidGroup = new Group();

	spaceShip = createSprite(70, windowHeight-100, 20, 20);
	spaceShip.addImage(spaceShipImg);
	spaceShip.scale = 1;

	spaceShip.y = windowHeight / 1
	spaceShip.x = windowWidth / 2
	spaceShip.scale = 0.6;
	spaceShip.visible = true;

}

function draw() {

	background(0, 0, 54);

	image(background2Img, 0, -x1, width, height);
	image(background2Img, 0, -x2, width, height);

	x1 -= scrollSpeed;
	x2 -= scrollSpeed;

	if (x1 < -height) {
		x1 = width;
	}

	if (x2 < -height) {
		x2 = width;
	}

	if (gameState === "START") {

		logo.visible = true;


		if (mousePressedOver(startButton)) {
			startButton.visible = false;
			logo.visible = false;
			pauseButton
			gameState = "PLAY";
		}

	}

	else if (gameState === "PLAY") {

		if (mousePressedOver(pauseButton)) {
			pause();
		}

		// creating boy running
		startButton.visible = false;
		coincount.visible = false;

		// spaceShip.visible = true;
		spaceShip.x = windowWidth / 2
		spaceShip.x = World.mouseX;

		logo.visible = false;
		playButton.visible = false;
		pauseButton.visible = true;

		edges = createEdgeSprites();
		spaceShip.collide(edges);


		createCash();
		createAsteroid();


		if (cashG.isTouching(spaceShip)) {
			cashG.destroyEach();
			treasureCollection = parseInt(treasureCollection)+20;
		}

		else if (asteroidGroup.isTouching(spaceShip)) {
			asteroidGroup.destroyEach();
			lives -= 1;
		}

		else if (lives === 0) {
			gameState = "END";
		}

		textSize(25);
		fill("gold");
		text("💰 " + treasureCollection, (windowWidth / 2) - 80, 110);

		textSize(25);
		fill("red");
		text("❤️ " + lives, windowWidth - 75, 30);

		textSize(25);
		fill("green");
		text("🌍 " + planet.charAt(0).toUpperCase() + planet.slice(1), 1 + 20, 30);

		

	}

	else if (gameState === "END") {

		if(treasureCollection >= 100) {
			gameState = "REDIRECTING";
			window.location = "/quiz?question=Q1&planet="+planet+"&coins="+treasureCollection;
		}
		else {
			gameState = "OVER";
		}
	}

	if(gameState === "PAUSE") {
		pauseButton.visible = false;
		playButton.visible = true;
		if(mousePressedOver(playButton)) {
			play();
		}
	}
	
	if(gameState === "OVER") {
		pauseButton.visible = false;
		resetButton.visible = true;
		spaceShip.x = windowWidth/2;
		spaceShip.y = windowHeight/2;
		spaceShip.addImage(gameoverImg);
		if(mousePressedOver(resetButton)) {
			reset();
		}
	}

	drawSprites();

}


function createCash() {
	if (World.frameCount % 200 == 0) {
		var cash = createSprite(Math.round(random(10, windowWidth), 40, 10, 10));
		cash.addImage(coinsImg);
		cash.scale = 1;
		cash.velocityY = SPEED;
		cash.lifetime = 200;
		cashG.add(cash);
	}
}

function createAsteroid() {

	if (World.frameCount % 20 == 0) {
		var asteroid = createSprite(Math.round(random(10, windowWidth), 40, 10, 10));

		//generate random obstacles
		var rand = Math.round(random(1, 5));
		switch (rand) {
			case 1: asteroid.addImage(asteroid1);
				break;
			case 2: asteroid.addImage(asteroid2);
				break;
			case 3: asteroid.addImage(asteroid3);
				break;
			case 4: asteroid.addImage(asteroid4);
				break;
			case 5: asteroid.addImage(asteroid5);
				break;
			default: break;
		}

		asteroid.scale = 1.3;
		asteroid.velocityY = SPEED;
		asteroid.lifetime = 200;
		asteroidGroup.add(asteroid);
	}
}

function pause() {
	pauseButton.visible = false;
	playButton.visible = true;
	gameState = "PAUSE";
}

function play() {
	pauseButton.visible = true;
	playButton.visible = false;
	gameState = "PLAY";
}

function reset() {
	level = 0;
	lives = 3;
	gameState = "START";
	window.location = "/game";
}


