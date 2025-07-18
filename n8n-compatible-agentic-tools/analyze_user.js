/**
 * ANALYZE_USER Tool
 * 
 * Description: Extract user activity data and engagement patterns
 * 
 * Use Cases:
 * - Assess user influence and expertise
 * - Understand posting patterns and timing
 * - Identify user's interests and communities
 * - Evaluate engagement quality and response rates
 * - Find potential collaboration opportunities
 * 
 * Input Schema:
 * {
 *   "username": {
 *     "type": "string",
 *     "description": "Reddit username without u/ prefix. Must be exact match to existing user."
 *   },
 *   "activity_limit": {
 *     "type": "integer", 
 *     "description": "Number of recent posts/comments to analyze (10-500). Default 100. Higher for deep analysis, lower for quick checks."
 *   },
 *   "content_types": {
 *     "type": "string",
 *     "description": "What to include: 'posts' (submissions only), 'comments' (comments only), 'both' (complete picture). Use 'both' for full analysis."
 *   },
 *   "subreddit_filter": {
 *     "type": "string",
 *     "description": "Comma-separated subreddits to focus on (e.g., 'london,ukjobs') or 'all' for complete activity. Use specific subreddits for targeted analysis."
 *   }
 * }
 * 
 * Example Input:
 * {
 *   "username": "london_recruiter",
 *   "activity_limit": 100,
 *   "content_types": "both",
 *   "subreddit_filter": "london,ukjobs"
 * }
 */

// Always validate query first
if (!query || typeof query !== 'object') {
  return `Error: Invalid input - query must be an object`;
}

if (!query.username) {
  return `Error: Missing required field: username`;
}

// TODO: Implement analyze_user functionality
// This will connect to the Reddit Scout API to fetch user data

return `analyze_user tool template - ready for implementation`;