import React from 'react';

const ReviewSection = ({ approved, setApproved, comments, setComments, onSubmit }) => {
    return (
        <div className="mt-8 p-6 bg-gray-50 border border-gray-300 rounded space-y-4">
            <h3 className="text-lg font-bold text-gray-800">Do you approve this post?</h3>
            <div className="flex space-x-4">
                <button
                    onClick={() => setApproved(true)}
                    className={`px-4 py-2 rounded-md text-white ${approved === true ? 'bg-green-600' : 'bg-green-500 hover:bg-green-600'}`}
                >
                    Approve
                </button>
                <button
                    onClick={() => setApproved(false)}
                    className={`px-4 py-2 rounded-md text-white ${approved === false ? 'bg-red-600' : 'bg-red-500 hover:bg-red-600'}`}
                >
                    Reject
                </button>
            </div>

            {approved === false && (
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Comments</label>
                    <textarea
                        value={comments}
                        onChange={(e) => setComments(e.target.value)}
                        rows={3}
                        className="w-full border border-gray-300 rounded p-2"
                        placeholder="Reason for rejection..."
                    />
                </div>
            )}

            {approved !== null && (
                <button
                    onClick={onSubmit}
                    className="mt-4 bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 font-semibold"
                >
                    Submit Review
                </button>
            )}
        </div>
    );
};

export default ReviewSection;
