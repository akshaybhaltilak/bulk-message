
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Config
login_time = 30                 # Time for login (in seconds)
new_msg_time = 5                # Time for a new message (in seconds)
send_msg_time = 5               # Time for sending a message (in seconds)
country_code = 91               # Set your country code
action_time = 2                 # Set time for button click action
image_path = 'image.png'        # Absolute path to your image

# Create driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Encode Message Text
with open('message.txt', 'r') as file:
    msg = file.read()

# Open browser with default link
link = 'https://web.whatsapp.com'
driver.get(link)
time.sleep(login_time)  # Time to scan QR code and login

# Wait function to ensure elements are clickable
def wait_for_element(selector, time=10):
    return WebDriverWait(driver, time).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
    )

# Loop Through Numbers List
with open('numbers.txt', 'r') as file:
    for n in file.readlines():
        num = n.rstrip()
        link = f'https://web.whatsapp.com/send/?phone={country_code}{num}'
        driver.get(link)
        time.sleep(new_msg_time)  # Wait for the chat to load

        try:
            # Click the attach button (Inspect the correct selector from WhatsApp Web)
            if image_path:
                attach_btn = wait_for_element('span[data-icon="clip"]')  # Updated CSS selector
                attach_btn.click()
                time.sleep(action_time)

                # Find and send image path to input (Inspect the correct input selector)
                msg_input = wait_for_element('input[type="file"]')  # Updated CSS selector for image input
                msg_input.send_keys(image_path)
                time.sleep(action_time)
        except Exception as e:
            print(f"Error while sending image: {e}")

        # Start the action chain to write the message
        actions = ActionChains(driver)
        for line in msg.split('\n'):
            actions.send_keys(line)
            # SHIFT + ENTER to create the next line in WhatsApp
            actions.key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT)
        actions.send_keys(Keys.ENTER)
        actions.perform()

        time.sleep(send_msg_time)  # Wait before moving to the next number

# Quit the driver
driver.quit()

# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time
# import threading
# import os
# import tensorflow as tf

# # Config for WhatsApp Bulk Sender
# login_time = 30  # Time for login (in seconds)
# new_msg_time = 3  # Reduced wait time for new messages
# send_msg_time = 2  # Reduced wait time for sending messages
# country_code = 91  # Set your country code

# # TensorFlow Lite Model Path (Optional)
# model_path = "model.tflite"
# use_tflite = False  # Flag to determine if we want to use TensorFlow Lite

# # Check if TensorFlow Lite model exists, only load if the file is available
# if os.path.exists(model_path):
#     interpreter = tf.lite.Interpreter(model_path=model_path)
#     interpreter.allocate_tensors()
#     use_tflite = True  # Set flag to true if model exists and is loaded
#     print("TensorFlow Lite model loaded successfully.")
# else:
#     print(f"Warning: The specified model file does not exist: {model_path}. Skipping model loading.")

# # Create WebDriver
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# # Read and encode the message text
# with open('message.txt', 'r') as file:
#     msg = file.read()

# # Open WhatsApp Web for login
# driver.get('https://web.whatsapp.com')
# time.sleep(login_time)  # Time to scan QR code and login

# # Wait function to ensure elements are clickable
# def wait_for_element(selector, time=10):
#     return WebDriverWait(driver, time).until(
#         EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
#     )

# # Function to send messages
# def send_message(num):
#     link = f'https://web.whatsapp.com/send/?phone={country_code}{num}'
#     driver.get(link)
#     time.sleep(new_msg_time)

#     # Write the message
#     actions = ActionChains(driver)
#     for line in msg.split('\n'):
#         actions.send_keys(line)
#         actions.key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT)  # SHIFT + ENTER for new line
#     actions.send_keys(Keys.ENTER).perform()  # Send the message

#     time.sleep(send_msg_time)  # Wait before moving to the next number

# # Multithreading for sending messages
# def send_messages_to_all(numbers):
#     threads = []
#     for num in numbers:
#         thread = threading.Thread(target=send_message, args=(num,))
#         thread.start()
#         threads.append(thread)

#     for thread in threads:
#         thread.join()

# # Read numbers from the file and send messages in parallel
# with open('numbers.txt', 'r') as file:
#     numbers = [n.rstrip() for n in file.readlines()]
#     send_messages_to_all(numbers)

# # Quit WebDriver after all messages are sent
# driver.quit()

# # TensorFlow Lite usage (if applicable)
# if use_tflite:
#     input_details = interpreter.get_input_details()
#     output_details = interpreter.get_output_details()

#     # Example: Run inference (if applicable)
#     # interpreter.set_tensor(input_details[0]['index'], your_input_data)
#     # interpreter.invoke()
#     # result = interpreter.get_tensor(output_details[0]['index'])
#     print("TensorFlow Lite model inference completed.")
