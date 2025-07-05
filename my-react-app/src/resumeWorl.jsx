import React, { useState, useRef } from 'react';

const ResumeWorkflow = () => {
    const [threadId, setThreadId] = useState('');
    const [comments, setComments] = useState('');
    const [approved, setApproved] = useState(true);
    const [streamOutput, setStreamOutput] = useState('');
    const eventSourceRef = useRef(null);

    const handleResume = async (e) => {
        e.preventDefault();

        if (!threadId.trim()) {
            alert('Thread ID is required.');
            return;
        }

        const data = { thread_id: threadId, comments, approved };

        try {
            if (eventSourceRef.current) {
                eventSourceRef.current.close();
            }

            const url = 'http://localhost:8000/api/agent/';
            const fetchOptions = {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            };

            const response = await fetch(url, fetchOptions);
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            setStreamOutput('');  // Clear previous

            while (true) {
                const { value, done } = await reader.read();
                if (done) break;
                const chunk = decoder.decode(value, { stream: true });
                setStreamOutput((prev) => prev + chunk);
            }
        } catch (err) {
            console.error('Error resuming workflow:', err);
            alert(`Error: ${err.message}`);
        }
    };

    return (
        <div className="max-w-xl mx-auto mt-10 p-6 bg-white shadow rounded">
            <h2 className="text-2xl font-bold mb-4 text-blue-600">Resume Workflow</h2>
            <form onSubmit={handleResume} className="space-y-4">
                <div>
                    <label className="block text-sm font-medium">Thread ID</label>
                    <input
                        type="text"
                        value={threadId}
                        onChange={(e) => setThreadId(e.target.value)}
                        className="w-full border rounded p-2"
                        required
                    />
                </div>

                <div>
                    <label className="block text-sm font-medium">Comments</label>
                    <textarea
                        value={comments}
                        onChange={(e) => setComments(e.target.value)}
                        className="w-full border rounded p-2"
                        rows={3}
                    />
                </div>

                <div className="flex items-center space-x-2">
                    <input
                        type="checkbox"
                        checked={approved}
                        onChange={(e) => setApproved(e.target.checked)}
                    />
                    <label className="text-sm">Approved</label>
                </div>

                <button
                    type="submit"
                    className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
                >
                    Resume Workflow
                </button>
            </form>

            {streamOutput && (
                <div className="mt-6">
                    <h3 className="font-semibold mb-2">Stream Output</h3>
                    <pre className="bg-gray-100 p-3 rounded text-sm whitespace-pre-wrap">
                        {streamOutput}
                    </pre>
                </div>
            )}
        </div>
    );
};

export default ResumeWorkflow;
