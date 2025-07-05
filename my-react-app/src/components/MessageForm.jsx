import React from 'react';

const MessageForm = ({
    message,
    includeImage,
    isStreaming,
    onChangeMessage,
    onChangeIncludeImage,
    onSubmit,
    onCancel,
}) => {
    return (
        <form onSubmit={onSubmit} className="space-y-6">
            <div>
                <label htmlFor="message" className="block text-gray-700 font-medium mb-2">Message</label>
                <input
                    type="text"
                    id="message"
                    value={message}
                    onChange={(e) => onChangeMessage(e.target.value)}
                    disabled={isStreaming}
                    required
                    className="w-full p-3 border border-gray-300 rounded-md shadow-sm focus:ring-2 focus:ring-blue-400"
                    placeholder="Enter a message for the agent..."
                />
            </div>

            <div className="flex items-center space-x-2">
                <input
                    type="checkbox"
                    id="includeImage"
                    checked={includeImage}
                    onChange={(e) => onChangeIncludeImage(e.target.checked)}
                    disabled={isStreaming}
                    className="h-5 w-5 text-blue-600"
                />
                <label htmlFor="includeImage" className="text-gray-700">Include Image</label>
            </div>

            <div className="flex space-x-4">
                <button
                    type="submit"
                    disabled={isStreaming || !message.trim()}
                    className={`flex-1 py-3 px-6 font-semibold text-white rounded-md shadow-md transition ${isStreaming ? 'bg-gray-400' : 'bg-blue-600 hover:bg-blue-700'}`}
                >
                    {isStreaming ? 'Sending...' : 'Send Message'}
                </button>

                {isStreaming && (
                    <button
                        type="button"
                        onClick={onCancel}
                        className="flex-1 py-3 px-6 bg-red-500 text-white rounded-md"
                    >
                        Cancel
                    </button>
                )}
            </div>
        </form>
    );
};

export default MessageForm;
