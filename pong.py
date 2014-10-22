# Implementation of classic arcade game Pong

#import gui and random modules
import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
ball_pos = [WIDTH/2, HEIGHT/2]
ball_vel = [-40.0 / 60.0,  4]
score1 = 0
score2 = 0
paddle1_pos = [[0, HEIGHT/2 - HALF_PAD_HEIGHT], [PAD_WIDTH, HEIGHT/2 - HALF_PAD_HEIGHT], [PAD_WIDTH, HEIGHT/2 + HALF_PAD_HEIGHT], [0, HEIGHT/2 + HALF_PAD_HEIGHT]]
paddle2_pos = [[WIDTH -1, HEIGHT/2 - HALF_PAD_HEIGHT], [WIDTH -1 -PAD_WIDTH, HEIGHT/2 - HALF_PAD_HEIGHT], [WIDTH -1 -PAD_WIDTH, HEIGHT/2 + HALF_PAD_HEIGHT], [WIDTH -1, HEIGHT/2 + HALF_PAD_HEIGHT]]
paddle1_vel, paddle2_vel = 0, 0
speed = 4

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    if direction == "RIGHT":
       ball_vel[0] = random.randrange(120, 240)/60
    if direction == "LEFT":
       ball_vel[0] = -random.randrange(120, 240)/60
    ball_vel[1] =  -random.randrange(60, 180)/60
    ball_pos = [WIDTH/2, HEIGHT/2]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    paddle1_pos = [[0, HEIGHT/2 - HALF_PAD_HEIGHT], [PAD_WIDTH, HEIGHT/2 - HALF_PAD_HEIGHT], [PAD_WIDTH, HEIGHT/2 + HALF_PAD_HEIGHT], [0, HEIGHT/2 + HALF_PAD_HEIGHT]]
    paddle2_pos = [[WIDTH -1, HEIGHT/2 - HALF_PAD_HEIGHT], [WIDTH -1 -PAD_WIDTH, HEIGHT/2 - HALF_PAD_HEIGHT], [WIDTH -1 -PAD_WIDTH, HEIGHT/2 + HALF_PAD_HEIGHT], [WIDTH -1, HEIGHT/2 + HALF_PAD_HEIGHT]]
    paddle1_vel, paddle2_vel = 0, 0
    score1, score2 = 0, 0
    spawn_ball("RIGHT")

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    if ball_pos[1] - BALL_RADIUS <= 0 or ball_pos[1] + BALL_RADIUS +1 >= HEIGHT:
        ball_vel[1] = -ball_vel[1]
        
	# TODO check if conditions     
    if ball_pos[0] - BALL_RADIUS <= PAD_WIDTH:
        if ball_pos[1] + BALL_RADIUS in range(paddle1_pos[0][1], paddle1_pos[3][1] +1) or ball_pos[1] - BALL_RADIUS in range(paddle1_pos[0][1], paddle1_pos[3][1] +1):
            ball_vel[0] = -1.1*ball_vel[0]
        else: 
            spawn_ball("RIGHT")
            score2 += 1
            
    if ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH:
        if ball_pos[1] + BALL_RADIUS in range(paddle2_pos[0][1], paddle2_pos[3][1] +1) or ball_pos[1] - BALL_RADIUS in range(paddle2_pos[0][1], paddle2_pos[3][1] +1):
            ball_vel[0] = -1.1*ball_vel[0]
        else: 
            spawn_ball("LEFT")
            score1 += 1
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos[0][1] + paddle1_vel >= 0 and paddle1_pos[3][1] + paddle1_vel <= HEIGHT:
        for i in range(0,4):
            paddle1_pos[i][1] += paddle1_vel 
    
    if paddle2_pos[0][1] + paddle2_vel >= 0 and paddle2_pos[3][1] + paddle2_vel <= HEIGHT:
        for i in range(0,4):
            paddle2_pos[i][1] += paddle2_vel 
    
    # draw paddles
    canvas.draw_polygon(paddle1_pos, 2, 'Grey', 'Blue')
    canvas.draw_polygon(paddle2_pos, 2, 'Grey', 'Red')

    # draw scores
    canvas.draw_text(str(score1), (WIDTH/2 -2*PAD_HEIGHT, 60), 50, 'Blue')
    canvas.draw_text(str(score2), (WIDTH/2 +2*PAD_HEIGHT -20, 60), 50, 'Red')
        
def keydown(key):
    global paddle1_vel, paddle2_vel, speed
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel -= speed
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel += speed
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel -= speed
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel += speed
   
def keyup(key):
    global paddle1_vel, paddle2_vel, speed
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel += speed
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel -= speed
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel += speed
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel -= speed

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game, 150)

# start frame
new_game()
frame.start()

