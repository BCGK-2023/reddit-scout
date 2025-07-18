# Reddit Scout - Project Summary

Reddit Scout is a Reddit scraper that can be hosted on Railway and uses API requests via `/api/scrape` with JSON body parameters to scrape Reddit content.

This project also includes agentic tools that can be used on MCP servers for AI agents on N8N.

## N8N Tool Node Rules

### Core Requirements:
- **Input**: Global variable `query` (contains the input data sent to your tool)
- **Output**: return 'string' (always return a string, never objects or arrays)
- **Language**: JavaScript
- **HTTP calls**: `this.helpers.httpRequest()` for external API calls

### Input Validation Pattern:
```javascript
// Always validate query first
if (!query || typeof query !== 'object') {
  return `Error: Invalid input - query must be an object`;
}

if (!query.requiredField) {
  return `Error: Missing required field: requiredField`;
}
```

### String-Based Input Pattern:
```javascript
// Use delimited strings for complex inputs
const languages = query.languages || 'python,javascript';
const langArray = languages.split(',').map(lang => lang.trim());

const criteria = query.criteria || '100,50,active';
const [minStars, minForks, activity] = criteria.split(',');
```

### N8N Tool Development Requirements:

#### 1. File Structure:
- Each tool must be a single `.js` file in `/n8n-compatible-agentic-tools/`
- File name format: `tool_name.js` (lowercase with underscores)
- Each file must be completely self-contained

#### 2. Documentation Standards:
- Include comprehensive JSDoc header with:
  - Tool description and purpose
  - Detailed use cases (3-5 examples)
  - Complete input schema with types and descriptions
  - Example input JSON with realistic values
  - Expected output format

#### 3. Error Handling:
- Always validate input parameters first
- Return descriptive error messages as strings
- Handle API failures gracefully
- Include field validation for required parameters

#### 4. API Integration:
- Use `this.helpers.httpRequest()` for all HTTP calls
- Implement proper error handling for network failures
- Return formatted string responses, not raw JSON objects
- Include timeout handling for long-running requests

#### 5. Response Format:
- Always return strings (use `JSON.stringify()` for complex data)
- Format responses for human readability when possible
- Include metadata like timestamps and source information
- Provide clear success/failure indicators

### Boilerplate Example:
```javascript
// Access input data
const name = query.name;
const age = query.age;

// Do something with it
const message = `Hello ${name}, you are ${age} years old!`;

// Return a string
return message;
```

### Input Schema Example:
```json
{
  "type": "object",
  "properties": {
    "name": { "type": "string", "description": "User's name" },
    "age": { "type": "number", "description": "User's age" }
  },
  "required": ["name", "age"]
}
```

**Input**: `{"name": "John", "age": 25}`
**Output**: `Hello John, you are 25 years old!`

---

# Reddit Scout N8N Tools Implementation Plan

## Project Overview & Philosophy

Reddit Scout is a foundational data extraction tool, not a complex AI analysis platform. It provides raw data primitives that AI agents can intelligently combine to build sophisticated workflows.

**Core Tools:**
- `view_subreddit` - Extract subreddit feeds with engagement metrics
- `analyze_user` - Get user activity patterns and influence metrics
- `search_content` - Search Reddit with advanced filters
- `extract_thread` - Get complete thread data with comment hierarchy
- `scan_user_batch` - Analyze multiple users for comparison

**Philosophy:** The tool does data extraction and basic metrics calculation. The AI agent handles interpretation, strategy, and connecting insights across multiple tool calls.

## Implementation Architecture

### **WHAT** - Core Components to Build

#### 1. FastAPI Web Server
- **Single endpoint architecture**: `POST /api` with tool routing
- **Auto-documentation**: OpenAPI/Swagger integration
- **Async support**: Handle concurrent requests efficiently
- **Type validation**: Automatic request/response validation

#### 2. Tool Implementation System
- **5 N8N Tools**: Complete implementation of all templated tools
- **Unified interface**: All tools use same request/response pattern
- **Schema validation**: JSON schema validation for all inputs
- **Error standardization**: Consistent error handling across tools

#### 3. Request/Response System
- **Single endpoint**: `POST /api` handles all tool requests
- **JSON body format**: `{"tool": "view_subreddit", "parameters": {...}}`
- **Response structure**: Consistent format with data + metadata
- **Error handling**: Detailed error messages for debugging

#### 4. Caching Layer
- **In-memory caching**: Simple Python dict with TTL
- **Cache expiration**: 5 minutes for subreddit data, 1 hour for user data
- **Performance optimization**: Reduce Reddit API calls
- **Memory management**: Automatic cleanup of expired entries

#### 5. Testing Framework
- **CLI testing tools**: Individual tool testing commands
- **Batch testing**: Test all tools with single command
- **Schema validation**: Ensure all responses match expected format
- **Integration testing**: Real Reddit API calls

#### 6. Docker Configuration
- **Railway-ready**: Optimized for Railway deployment
- **Proxy integration**: Uses existing Railway proxy setup
- **Environment variables**: Railway-friendly configuration
- **Health checks**: `/health` endpoint for monitoring

### **WHY** - Strategic Reasoning

#### Single Endpoint Design
- **Simplicity**: Easier N8N integration and maintenance
- **Consistency**: All tools follow same request pattern
- **Flexibility**: Easy to add new tools without changing API structure
- **Debugging**: Centralized logging and error handling

#### Stateless Architecture
- **Railway-friendly**: No database dependencies
- **Scalability**: Easy horizontal scaling
- **Reliability**: No state corruption issues
- **Simplicity**: Reduced operational complexity

#### Proxy Integration
- **Existing setup**: Leverages Railway proxy configuration
- **Rate limiting**: Proxy handles Reddit rate limits
- **Reliability**: Proxy rotation prevents IP bans
- **Performance**: Optimized routing and caching

#### Raw Data Focus
- **Agent flexibility**: AI agents interpret and combine data
- **Simplicity**: Focus on extraction, not analysis
- **Modularity**: Tools can be combined in various ways
- **Performance**: Lightweight processing, faster responses

#### FastAPI Choice
- **Auto-documentation**: Built-in OpenAPI/Swagger docs
- **Async support**: Better performance for I/O operations
- **Type validation**: Automatic request/response validation
- **Modern Python**: Best practices and performance

### **HOW** - Technical Implementation

#### Project Structure
```
reddit-scout/
├── api/
│   ├── __init__.py
│   ├── main.py              # FastAPI server
│   ├── models.py            # Pydantic models for validation
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── view_subreddit.py
│   │   ├── analyze_user.py
│   │   ├── search_content.py
│   │   ├── extract_thread.py
│   │   └── scan_user_batch.py
│   ├── utils.py             # Caching, helpers
│   └── cache.py             # In-memory cache implementation
├── test_tools.py            # CLI testing framework
├── Dockerfile               # Railway deployment
└── requirements.txt         # Dependencies
```

#### API Endpoints
- `POST /api` - Execute any tool
- `GET /api/logs` - View recent API calls
- `GET /health` - Health check
- `GET /docs` - Auto-generated API documentation

#### Tool Request Format
```json
{
  "tool": "view_subreddit",
  "parameters": {
    "subreddit_name": "entrepreneur",
    "post_limit": 25,
    "sort_method": "hot",
    "time_filter": "week",
    "include_comments": true
  }
}
```

#### Response Format
```json
{
  "success": true,
  "data": {
    "subreddit_meta": {...},
    "posts": [...],
    "engagement_patterns": {...}
  },
  "metadata": {
    "execution_time": 2.34,
    "cached": false,
    "timestamp": "2024-07-18T16:00:00Z"
  }
}
```

#### Error Response Format
```json
{
  "success": false,
  "error": {
    "type": "ValidationError",
    "message": "Missing required field: subreddit_name",
    "details": {...}
  },
  "metadata": {
    "execution_time": 0.01,
    "timestamp": "2024-07-18T16:00:00Z"
  }
}
```

#### Caching Strategy
- **Key format**: `{tool}:{hash(parameters)}`
- **TTL settings**: Configurable per tool type
- **Memory management**: LRU eviction when limit reached
- **Cache invalidation**: Time-based expiration

#### Testing Commands
```bash
# Test individual tools
python test_tools.py view_subreddit --subreddit=entrepreneur --limit=5
python test_tools.py analyze_user --username=spez --limit=10

# Test all tools
python test_tools.py --all

# Validate schemas
python test_tools.py --validate-schemas
```

#### Environment Configuration
```bash
# Railway Environment Variables
PROXY_ENABLED=true
PROXY_HOST=your-proxy-host
PROXY_PORT=8080
PROXY_USERNAME=username
PROXY_PASSWORD=password

# API Configuration
API_PORT=8000
LOG_LEVEL=INFO
CACHE_TTL_SUBREDDIT=300
CACHE_TTL_USER=3600
```

## Implementation Phases

### **Phase 1: Core API Server**
1. **FastAPI setup** - Basic server with health check
2. **Tool routing** - Single endpoint with tool parameter
3. **Basic implementations** - All 5 tools with minimal functionality
4. **Schema validation** - Request/response validation
5. **Error handling** - Consistent error responses

### **Phase 2: Advanced Features**
1. **Caching layer** - In-memory caching with TTL
2. **Analytics calculations** - Engagement metrics and patterns
3. **Batch processing** - Optimized multi-user analysis
4. **Logging system** - API request/response logging
5. **Performance optimization** - Async processing and connection pooling

### **Phase 3: Testing & Documentation**
1. **CLI testing framework** - Individual and batch testing
2. **Schema validation** - Ensure all responses match expected format
3. **Integration testing** - Real Reddit API calls
4. **Documentation** - API usage examples and guides
5. **Docker optimization** - Railway-ready deployment configuration

## Tool Implementation Details

### 1. view_subreddit Tool
**Purpose**: Extract subreddit feeds with engagement metrics
**Implementation**: Uses existing `fetch_subreddit_posts()` + analytics calculations
**Analytics**: Average scores, active hours, content type distribution
**Cache TTL**: 5 minutes

### 2. analyze_user Tool
**Purpose**: Get user activity patterns and influence metrics
**Implementation**: Uses existing `scrape_user_data()` + pattern analysis
**Analytics**: Response rate, posting frequency, expertise indicators
**Cache TTL**: 1 hour

### 3. search_content Tool
**Purpose**: Search Reddit with advanced filters
**Implementation**: Uses existing `search_reddit()` + filtering
**Analytics**: Sentiment distribution, temporal patterns, relevance scoring
**Cache TTL**: 10 minutes

### 4. extract_thread Tool
**Purpose**: Get complete thread data with comment hierarchy
**Implementation**: Uses existing `scrape_post_details()` + thread analysis
**Analytics**: Discussion duration, participant analysis, engagement flow
**Cache TTL**: 30 minutes

### 5. scan_user_batch Tool
**Purpose**: Analyze multiple users for comparison
**Implementation**: Batch processing of `analyze_user` + comparison logic
**Analytics**: Influence ranking, expertise comparison, activity patterns
**Cache TTL**: 2 hours

## Success Metrics

### Technical Metrics
- **Response time**: < 5 seconds for standard requests
- **Error rate**: < 1% for valid requests
- **Cache hit rate**: > 60% for repeated requests
- **Uptime**: > 99.9% availability

### Functional Metrics
- **Schema compliance**: 100% response validation
- **Tool coverage**: All 5 tools fully implemented
- **Error handling**: Comprehensive error coverage
- **Documentation**: Complete API documentation

This implementation plan provides a clear roadmap for building a robust, scalable Reddit Scout API that seamlessly integrates with N8N workflows while maintaining simplicity and performance.

---

## Development Rules & Progress Tracking

### **Code Documentation Rules**
- **Always add comments** when building features from this implementation plan
- **Non-destructive commenting** - Add explanatory comments without changing existing functionality
- **Progress indicators** - Use comments to mark implementation progress and completion status
- **Feature mapping** - Link code comments back to specific sections of this implementation plan
- **Development notes** - Include reasoning, decisions, and future considerations in comments

### **Comment Standards**
```python
# ✅ IMPLEMENTED: Phase 1 - FastAPI setup (see Implementation Plan)
# 🔄 IN PROGRESS: Adding caching layer for subreddit data
# 📋 TODO: Implement batch processing optimization
# 🔗 PLAN REF: Implementation Plan -> Phase 2 -> Caching layer
```

### **Progress Tracking**
As features are built, update this plan with:
- ✅ **Completed features** - Mark with completion date
- 🔄 **In progress** - Current development status
- 📋 **Planned** - Next features to implement
- 🔗 **Cross-references** - Link between plan and actual code

This ensures the implementation plan remains a living document that reflects actual development progress and helps maintain alignment between planning and execution.