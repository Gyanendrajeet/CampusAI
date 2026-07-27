import { useState } from "react";

function ChatBox() {

  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const sendMessage = async () => {

    if (!question) {
      return;
    }

    try {

      const response = await fetch(
        `http://127.0.0.1:8000/chat?user_id=5&question=${question}&answer=AI%20response%20generated`,
        {
          method: "POST",
          headers: {
            "accept": "application/json"
          }
        }
      );

      const data = await response.json();

      setAnswer(
        "Saved: " + data.message
      );

      setQuestion("");

    } catch (error) {

      setAnswer("Backend connection error");

    }
  };


  return (
    <div>
      <h2>AI Chat</h2>

      <input
        type="text"
        placeholder="Ask something..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      <button onClick={sendMessage}>
        Send
      </button>

      <p>{answer}</p>

    </div>
  );
}

export default ChatBox;