import React, { useState, useRef } from 'react';
import MessageForm from './MessageForm';
import StreamOutput from './StreamOutput';
import ThreadInfo from './ThreadInfo';
import ReviewSection from './ReviewSection';

const SocialMediaAgent = () => {
    const [message, setMessage] = useState('');
    const [includeImage, setIncludeImage] = useState(false);
    const [isStreaming, setIsStreaming] = useState(false);
    const [threadId, setThreadId] = useState(localStorage.getItem('threadId') || null);
    const [streamedData, setStreamedData] = useState('');
    const [process, setProcess] = useState(null);
    const [reviewPhase, setReviewPhase] = useState(false);
    const [approved, setApproved] = useState(null);
    const [comments, setComments] = useState('');
    const abortControllerRef = useRef(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsStreaming(true);
        setStreamedData('');
        setThreadId(null);
        setReviewPhase(false);
        setApproved(null);
        setComments('');

        try {
            abortControllerRef.current = new AbortController();
            const response = await fetch('http://localhost:8000/api/agent/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message, include_image: includeImage }),
                signal: abortControllerRef.current.signal
            });

            const receivedThreadId = response.headers.get('X-Thread-ID');
            console.log('Received Thread ID:', response.headers);
            if (receivedThreadId) {
                localStorage.setItem('threadId', receivedThreadId);
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
                    setProcess('Please Review the post');
                    setStreamedData(prev => prev + chunk);
                }

            }

            setReviewPhase(true);
        } catch (err) {
            console.error(err);
            if (err.name !== 'AbortError') alert('Error: ' + err.message);
        } finally {
            setIsStreaming(false);
            abortControllerRef.current = null;
        }
    };

    const handleReviewSubmit = async () => {
        const payload = {
            thread_id: threadId,
            approved,
            comments: approved ? '' : comments
        };

        const response = await fetch('http://localhost:8000/api/agent/', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;
            const chunk = decoder.decode(value, { stream: true });
            if (chunk.startsWith('data: ')) {
                setProcess(chunk.split('data: ')[1].trim());
            } else {
                setProcess('Please Review the post');
                setStreamedData(chunk + 128);
            }
        }
        setReviewPhase(false);
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-100 to-purple-100 p-6 font-sans">
            <div className="max-w-3xl mx-auto bg-white p-8 rounded-lg shadow-lg border border-gray-200">
                <h1 className="text-3xl font-bold mb-6 text-blue-700 text-center">Social Media Agent</h1>

                <MessageForm
                    message={message}
                    includeImage={includeImage}
                    isStreaming={isStreaming}
                    onChangeMessage={setMessage}
                    onChangeIncludeImage={setIncludeImage}
                    onSubmit={handleSubmit}
                    onCancel={() => abortControllerRef.current?.abort()}
                />

                <StreamOutput process={process} streamedData={streamedData} />

                {reviewPhase && (
                    <ReviewSection
                        approved={approved}
                        setApproved={setApproved}
                        comments={comments}
                        setComments={setComments}
                        onSubmit={handleReviewSubmit}
                    />
                )}
            </div>
        </div>
    );
};

export default SocialMediaAgent;
