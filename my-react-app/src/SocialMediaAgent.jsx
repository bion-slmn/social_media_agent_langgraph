import React, { useState, useRef } from 'react';

const SocialMediaAgent = () => {
    const [message, setMessage] = useState('');
    const [includeImage, setIncludeImage] = useState(false);
    const [isStreaming, setIsStreaming] = useState(false);
    const [threadId, setThreadId] = useState(null);
    const [streamedData, setStreamedData] = useState('');
    const abortControllerRef = useRef(null);
    const [process, setProcess] = useState(null);

    const cleanData = (data) => {


        console.log('Received data:', data);
        const { query, ideas } = data;

        // Parse ideas by [[END]]
        const parsedIdeas = ideas
            .split('[[END]]')
            .map((idea, index) => idea.trim())
            .filter(Boolean);
        return parsedIdeas
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!message.trim() || isStreaming) return;

        setIsStreaming(true);
        setStreamedData('');
        setThreadId(null);

        try {
            abortControllerRef.current = new AbortController();

            const response = await fetch('http://localhost:8000/api/agent/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message, include_image: includeImage }),
                signal: abortControllerRef.current.signal
            });

            const receivedThreadId = response.headers.get('X-Thread-ID');
            if (receivedThreadId) {
                setThreadId(receivedThreadId);
            }

            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            while (true) {
                const { value, done } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value, { stream: true });
                if (chunk.startsWith('data: ')) {
                    setProcess(chunk.split('data: ')[1].trim());
                } else {
                    setProcess('Please Review. the post');
                    console.log('Chunk received:', typeof chunk);
                    //const cleanedData = cleanData(chunk);
                    setStreamedData(chunk);
                }

            }
        } catch (error) {
            if (error.name !== 'AbortError') {
                console.error('Error:', error);
                alert(`Error: ${error.message}`);
            }
        } finally {
            setIsStreaming(false);
            abortControllerRef.current = null;
        }
    };

    const cancelRequest = () => {
        if (abortControllerRef.current) {
            abortControllerRef.current.abort();
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-100 to-purple-100 p-6 font-sans">
            <div className="max-w-3xl mx-auto bg-white p-8 rounded-lg shadow-lg border border-gray-200">
                <h1 className="text-3xl font-bold mb-6 text-blue-700 text-center">Social Media Agent</h1>

                <form onSubmit={handleSubmit} className="space-y-6">
                    <div>
                        <label htmlFor="message" className="block text-gray-700 font-medium mb-2">
                            Message
                        </label>
                        <textarea
                            id="message"
                            value={message}
                            onChange={(e) => setMessage(e.target.value)}
                            rows={4}
                            disabled={isStreaming}
                            required
                            className="w-full p-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-blue-400"
                            placeholder="Enter a message for the agent..."
                        />
                    </div>

                    <div className="flex items-center space-x-2">
                        <input
                            type="checkbox"
                            id="includeImage"
                            checked={includeImage}
                            onChange={(e) => setIncludeImage(e.target.checked)}
                            disabled={isStreaming}
                            className="h-5 w-5 text-blue-600 border-gray-300 rounded"
                        />
                        <label htmlFor="includeImage" className="text-gray-700">Include Image</label>
                    </div>

                    <div className="flex space-x-4">
                        <button
                            type="submit"
                            disabled={isStreaming || !message.trim()}
                            className={`flex-1 py-3 px-6 font-semibold text-white rounded-md shadow-md transition ${isStreaming ? 'bg-gray-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'
                                }`}
                        >
                            {isStreaming ? 'Sending...' : 'Send Message'}
                        </button>

                        {isStreaming && (
                            <button
                                type="button"
                                onClick={cancelRequest}
                                className="flex-1 py-3 px-6 bg-red-500 hover:bg-red-600 text-white font-semibold rounded-md shadow-md transition"
                            >
                                Cancel
                            </button>
                        )}
                    </div>
                </form>

                {threadId && (
                    <div className="mt-6 p-4 bg-green-100 text-green-800 rounded-md border border-green-300 font-mono">
                        <strong>Thread ID:</strong> {threadId}
                    </div>
                )}

                {process && (
                    <div className="mt-6">
                        <h3 className="text-xl font-semibold text-gray-800 mb-2">Stream Response : {process}</h3>
                        <div className="bg-gray-100 border border-gray-300 p-4 rounded-md h-64 overflow-y-auto font-mono text-sm whitespace-pre-wrap">
                            {streamedData}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};


const PostIdeas = ({ data }) => {
    const { query, ideas } = data;

    // Parse ideas by [[END]]
    const parsedIdeas = ideas
        .split('[[END]]')
        .map((idea, index) => idea.trim())
        .filter(Boolean); // remove empty strings

    return (
        <div className="mt-8 p-6 bg-white rounded-lg shadow border border-gray-200">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">{query}</h2>

            <ul className="space-y-6">
                {parsedIdeas.map((idea, idx) => (
                    <li
                        key={idx}
                        className="p-4 bg-gray-50 border border-gray-300 rounded-lg shadow-sm"
                    >
                        <div className="text-gray-700 whitespace-pre-wrap">{idea}</div>
                    </li>
                ))}
            </ul>
        </div>
    );
};




export default SocialMediaAgent;

