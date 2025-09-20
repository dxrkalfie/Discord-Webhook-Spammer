import customtkinter as ctk
from tkinter import messagebox
import requests
import threading
import time


FOOTER_TEXT = "\n\n-# Made By Dxrk" ## Remove this if you dont want to have This! (Only for some credit yk)

def verify_webhook(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("name", "Unknown")
        else:
            return None
    except:
        return None

def delete_webhook(url):
    try:
        response = requests.delete(url)
        if response.status_code == 204:
            messagebox.showinfo("Success", "Webhook successfully deleted!")
        else:
            messagebox.showerror("Error", "Failed to delete webhook.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def spam_webhook(url, message, delay, amount, log_box, stop_flag):
    count = 0
    full_message = message + FOOTER_TEXT

    if not message.strip():
        log_box.insert("end", "[!] Message cannot be empty.\n")
        log_box.see("end")
        return

    try:
        while not stop_flag[0]:
            log_box.insert("end", f"[>] Sending message:\n{full_message}\n")
            log_box.see("end")

            response = requests.post(url, json={"content": full_message})
            if response.status_code in (200, 204):
                count += 1
                log_box.insert("end", f"[✓] Message sent ({count})\n")
                log_box.see("end")
            else:
                log_box.insert("end", f"[✗] Failed ({response.status_code})\n")
                log_box.see("end")

            if amount > 0 and count >= amount:
                log_box.insert("end", "[✓] Spam complete.\n")
                log_box.see("end")
                break

            time.sleep(delay)

    except Exception as e:
        log_box.insert("end", f"[✗] Error: {str(e)}\n")
        log_box.see("end")

# --- GUI ---

def start_gui():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Webhook Tool")
    root.geometry("800x1000")

    stop_flag = [False]
    active_webhook = [None]

    frame = ctk.CTkFrame(root, corner_radius=15)
    frame.pack(padx=20, pady=20, fill="both", expand=False)

    url_label = ctk.CTkLabel(frame, text="Webhook URL:", font=("Arial", 16))
    url_label.pack(pady=5)
    url_entry = ctk.CTkEntry(frame, width=600, height=35)
    url_entry.pack(pady=5)

    webhook_name_label = ctk.CTkLabel(frame, text="Webhook Name: Unknown", text_color="cyan", font=("Arial", 14))
    webhook_name_label.pack(pady=5)

    def connect_webhook():
        url = url_entry.get().strip()
        name = verify_webhook(url)
        if name:
            webhook_name_label.configure(text=f"Webhook Name: {name}")
            active_webhook[0] = url
            messagebox.showinfo("Connected", f"Webhook '{name}' is valid and selected.")
        else:
            active_webhook[0] = None
            messagebox.showerror("Error", "Invalid webhook URL!")

    connect_button = ctk.CTkButton(frame, text="Connect", command=connect_webhook, width=200, height=40)
    connect_button.pack(pady=10)

    spam_frame = ctk.CTkFrame(root, corner_radius=15)
    spam_frame.pack(padx=20, pady=10, fill="both", expand=False)

    ctk.CTkLabel(spam_frame, text="Spam Message (use Enter or \n for new lines):", font=("Arial", 14)).pack(pady=5)
    message_entry = ctk.CTkTextbox(spam_frame, width=600, height=100)
    message_entry.pack(pady=5)

    ctk.CTkLabel(spam_frame, text="Delay (seconds):", font=("Arial", 14)).pack(pady=5)
    delay_entry = ctk.CTkEntry(spam_frame, width=100, height=30)
    delay_entry.insert(0, "1")
    delay_entry.pack(pady=5)

    ctk.CTkLabel(spam_frame, text="Number of Messages (0 = infinite):", font=("Arial", 14)).pack(pady=5)
    amount_entry = ctk.CTkEntry(spam_frame, width=100, height=30)
    amount_entry.insert(0, "10")
    amount_entry.pack(pady=5)

    log_box = ctk.CTkTextbox(root, width=750, height=300)
    log_box.pack(pady=10)

    def start_spam():
        if not active_webhook[0]:
            messagebox.showerror("Error", "No valid webhook connected!")
            return

        stop_flag[0] = False
        url = active_webhook[0]
        try:
            delay = float(delay_entry.get())
            amount = int(amount_entry.get())
            message = message_entry.get("1.0", "end-1c")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for delay/amount")
            return

        threading.Thread(target=spam_webhook, args=(url, message, delay, amount, log_box, stop_flag), daemon=True).start()

    def stop_spam():
        stop_flag[0] = True

    def delete():
        url = active_webhook[0]
        if url and verify_webhook(url):
            delete_webhook(url)
            active_webhook[0] = None
        else:
            messagebox.showerror("Error", "No valid webhook connected!")

    button_frame = ctk.CTkFrame(root, corner_radius=15)
    button_frame.pack(padx=20, pady=20, fill="x")

    ctk.CTkButton(button_frame, text="Start Spamming", command=start_spam, fg_color="green", width=200, height=50).pack(side="left", padx=20, pady=10, expand=True)
    ctk.CTkButton(button_frame, text="Stop Spam", command=stop_spam, fg_color="orange", width=200, height=50).pack(side="left", padx=20, pady=10, expand=True)
    ctk.CTkButton(button_frame, text="Delete Webhook", command=delete, fg_color="red", width=200, height=50).pack(side="left", padx=20, pady=10, expand=True)

    root.mainloop()

if __name__ == "__main__":
    start_gui()
