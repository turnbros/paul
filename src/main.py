import os
import asyncio
import api_web
import api_lang
import threading
import intent_routes       

from workflows import server_count
from workflows import server_update


bind_ip = os.getenv("BIND_IP", "0.0.0.0")
bind_port = int(os.getenv("BIND_PORT", 8443))
debug_mode = bool(os.getenv("DEBUG_PAUL", False)) # Yes, any ENV var value will cause Paul to run in debug.
discord_token = os.getenv("DISCORD_TOKEN") # TODO: Raise error if None


if __name__ == "__main__":
    
    # Register the intent workflows
    intent_routes.register_intent_workflow("server_count")
    intent_routes.register_intent_workflow("server_update")
    
    server_count_loop = asyncio.new_event_loop()
    server_count_task = server_count_loop.create_task(server_count.worker_main())
    threading.Thread(name="server_count_worker", target=lambda: server_count_loop.run_forever()).start()

    server_update_loop = asyncio.new_event_loop()
    server_update_task = server_update_loop.create_task(server_update.worker_main())
    threading.Thread(name="server_update_worker", target=lambda: server_update_loop.run_forever()).start()

    threading.Thread(name="flask", target=lambda: api_web.app.run(host=bind_ip, port=bind_port, debug=debug_mode)).start()

    # discord_loop = asyncio.new_event_loop()
    # discord_task = discord_loop.create_task(api_lang.start_client(discord_token))
    # threading.Thread(name="discord", target=lambda: discord_loop.run_forever()).start()
    
    #while True:
    #    pass

    api_lang.start_client(discord_token)