var canvas = document.getElementById("myCanvas");
var ctx = canvas.getContext("2d");

// Balle
var ballRadius = 10;
var xBall = canvas.width/2;
var yBall = canvas.height/2;
var speedBall = 5;
var maxSpeedBall = 6;
var dx = speedBall;
var dy = speedBall;

// Paddle
var paddleHeight = 75;
var paddleWidth = 10;

// Joueur1
var paddleYJ1 = (canvas.height-paddleHeight)/2;
var paddleXJ1 = 2;
var speedPaddleJ1 = 3;
var upPressed = false;
var downPressed = false;
var scorej1 = 0;

// Joueur2
var paddleYJ2 = (canvas.height-paddleHeight)/2;
var paddleXJ2 = canvas.width-paddleWidth-2;
var speedPaddleJ2 = 3;
var upIA = false;
var downIA = false;
var scorej2 = 0;

document.addEventListener("keydown", keyDownHandler, false);
document.addEventListener("keyup", keyUpHandler, false);

function keyDownHandler(e) {
    if(e.keyCode == 38) {
      upPressed = true;
    }
    else if(e.keyCode == 40) {
      downPressed = true;
    }
}

function keyUpHandler(e) {
    if(e.keyCode == 38) {
        upPressed = false;
    }
    else if(e.keyCode == 40) {
        downPressed = false;
    }
}

function drawJ1() {
    ctx.beginPath();
    ctx.rect(paddleXJ1, paddleYJ1, paddleWidth, paddleHeight);
    ctx.fillStyle = "#FFFFFF";
    ctx.fill();
    ctx.closePath();
}

function drawJ2() {
    ctx.beginPath();
    ctx.rect(paddleXJ2, paddleYJ2, paddleWidth, paddleHeight);
    ctx.fillStyle = "#FFFFFF";
    ctx.fill();
    ctx.closePath();
}

function drawBall() {
    ctx.beginPath();
    ctx.arc(xBall, yBall, ballRadius, 0, Math.PI*2);
    ctx.fillStyle = "#FFFFFF";
    ctx.fill();
    ctx.closePath();
}

function drawScore() {
    ctx.font = "66px Arial";
    ctx.fillStyle = "#FFFFFF";
    ctx.fillText(scorej1, 100, 66);
    ctx.fillText(scorej2, canvas.width-125, 66);
}

function collisionBallPlayer()
{
    // Collision joueur1
    if(xBall + dx - ballRadius >= paddleXJ1 + paddleWidth/2 && xBall + dx - ballRadius <= paddleXJ1 + paddleWidth ) {
        if (yBall >= paddleYJ1 && yBall <= paddleYJ1 + paddleHeight*(2/5))
        {
            dx = -dx;
            if (dy != -speedBall)
            {
                dy = -speedBall;
            }
        }
        else if (yBall > paddleYJ1 + paddleHeight*(2/5) && yBall < paddleYJ1 + paddleHeight*(3/5))
        {
            dx = -dx;
            if (dy != 0)
            {
                dy = 0;
            }
        }
        else if (yBall >= paddleYJ1 + paddleHeight*(3/5) && yBall <= paddleYJ1 + paddleHeight)
        {
            dx = -dx;
            if (dy != speedBall)
            {
                dy = speedBall;
            }
        }
    }

    // Collision joueur2
    if(xBall + dx + ballRadius >= paddleXJ2 + paddleWidth/2 && xBall + dx + ballRadius <= paddleXJ2 + paddleWidth ) {
        if (yBall > paddleYJ2 && yBall < paddleYJ2 + paddleHeight)
        {
            dx = -dx;
        }
    }

    // Collision mur
    if(yBall + dy < ballRadius || yBall + dy > canvas.height - ballRadius)
    {
        dy = -dy;
    }
}

function IA()
{
    if( yBall < paddleYJ2 + paddleHeight/2 )
    {
        upIA = true;
        downIA = false;
    }
    else if( yBall > paddleYJ2 + paddleHeight/2)
    {
        upIA = false;
        downIA = true;
    }
    else
    {
        upIA = false;
        downIA = false;
    }
}

function gameOver()
{
    if( xBall < 0)
    {
        alert('Game Over !');
        clearInterval(interval); // Needed for Chrome to end game
    }
    if ( xBall > canvas.width)
    {
        scorej1 += 1;
        xBall = canvas.width*(3/4);
        yBall = canvas.height/2;

        if(dx + 1 <= maxSpeedBall)
        {
            dx += 1;
            speedPaddleJ2 += 1;
        }

        dx = -dx;
        
    }
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawScore();
    drawJ1();
    drawJ2();
    drawBall();
    
    collisionBallPlayer();
    gameOver();

    // Déplacement Joueur
    if (upPressed){
        if( paddleYJ1 - speedPaddleJ1 < 0)
        {
            paddleYJ1 = 0;
        }
        else{
            paddleYJ1 -= speedPaddleJ1;
        }
    }
    if (downPressed){
        if (paddleYJ1 + paddleHeight + speedPaddleJ1 > canvas.height)
        {
            paddleYJ1 = canvas.height - paddleHeight;
        }
        else{
            paddleYJ1 += speedPaddleJ1;
        }
    }

    // Déplacement IA
    IA();
    if(upIA)
    {
        if( paddleYJ2 - speedPaddleJ2 < 0)
        {
            paddleYJ2 = 0;
        }
        else{
            paddleYJ2 -= speedPaddleJ2;
        }
    }
    if (downIA)
    {
        if (paddleYJ2 + paddleHeight + speedPaddleJ2 > canvas.height)
        {
            paddleYJ2 = canvas.height - paddleHeight;
        }
        else{
            paddleYJ2 += speedPaddleJ2;
        }
    }
    xBall += dx;
    yBall += dy;
}

function add_score() {
    //Création dynamique du formulaire
    var form = document.createElement('form');
    form.method = 'POST';
    form.action = 'add_score';
  
    var scoreInput = document.createElement('input');
    scoreInput.type = 'HIDDEN';
    scoreInput.name = 'score';
    scoreInput.value = scorej1;
  
    var game = document.createElement('input');
    game.type = 'HIDDEN';
    game.name = 'game';
    game.value = 'Pong'
    
    form.appendChild(scoreInput);
    form.appendChild(game);
    //Ajout du formulaire à la page et soumission du formulaire
    document.body.appendChild(form);
  
    form.submit();
}  


var interval = setInterval(draw, 10);
  