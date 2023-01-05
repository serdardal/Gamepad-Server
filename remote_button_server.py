import json
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.websocket
import tornado.options
import tornado.escape
import vgamepad as vg

LISTEN_PORT = 8000
LISTEN_ADDRESS = '192.168.2.209'

gamepad = vg.VX360Gamepad()

class GamepadHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)

        self.buttonsDict = {
            1: vg.XUSB_BUTTON.XUSB_GAMEPAD_A,
            2: vg.XUSB_BUTTON.XUSB_GAMEPAD_B,
            3: vg.XUSB_BUTTON.XUSB_GAMEPAD_X,
            4: vg.XUSB_BUTTON.XUSB_GAMEPAD_Y,
            5: vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP,
            6: vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN,
            7: vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT,
            8: vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT,
            9: vg.XUSB_BUTTON.XUSB_GAMEPAD_START,
            10: vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK
        }

    @classmethod
    def route_urls(cls):
        return [(r'/gamepad',cls, {}),]
        
    def open(self):
        print("new client connected")
        self.write_message("you are connected")
        
    def on_message(self, message):
        print("received message {}".format(message))

        data = json.loads(message)
        button = data["button"]
        pushed = data["pushed"]

        if button in self.buttonsDict:
            if pushed:
                gamepad.press_button(self.buttonsDict[button])
            else:
                gamepad.release_button(self.buttonsDict[button])
            gamepad.update()
        else:
            print("invalid message received")
            self.write_message("invalid message")
    
    def on_close(self):
        print("connection is closed")
    
    def check_origin(self, origin):
        return True
    
    
def main():
    app = tornado.web.Application(GamepadHandler.route_urls(), websocket_ping_interval=10)
    
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(LISTEN_PORT, LISTEN_ADDRESS)

    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()