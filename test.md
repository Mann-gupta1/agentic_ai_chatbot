# Test Cases for Agentic AI System


## Direct Agent Tests

### Test Case 1.1: Simple Mathematical Calculations
**Objective**: Verify Direct Agent handles basic arithmetic correctly
**Steps**:
1. Send query: "What is 15 + 27?"
2. Send query: "Calculate 144 divided by 12"
**Expected Result**: Returns correct mathematical results (42 and 12 respectively)
**Pass Criteria**: Accurate calculations, quick response time

### Test Case 1.2: Basic Information Queries
**Objective**: Verify Direct Agent handles simple factual questions
**Steps**:
1. Send query: "What is the capital of India?"
2. Send query: "How many days are in a leap year?"
**Expected Result**: Returns correct answers (New Delhi and 366 respectively)
**Pass Criteria**: Accurate information, appropriate routing to Direct Agent

## Knowledge Agent Tests

### Test Case 2.1: Complex Educational Content
**Objective**: Verify Knowledge Agent provides detailed explanations
**Steps**:
1. Send query: "Explain the process of photosynthesis in detail"
2. Send query: "What are the principles of quantum mechanics?"
**Expected Result**: Comprehensive, educational responses with proper depth
**Pass Criteria**: Detailed explanations, scientifically accurate content

### Test Case 2.2: Multi-Topic Knowledge Synthesis
**Objective**: Verify Knowledge Agent can combine information from multiple domains
**Steps**:
1. Send query: "How does climate change affect marine ecosystems?"
2. Send query: "Explain the historical development of artificial intelligence"
**Expected Result**: Well-structured responses combining multiple knowledge areas
**Pass Criteria**: Comprehensive answers, proper topic integration

## Reasoning Agent Tests

### Test Case 3.1: Multi-Step Problem Solving
**Objective**: Verify Reasoning Agent can solve complex problems requiring multiple steps
**Steps**:
1. Send query: "If a train travels 60 mph for 2 hours, then 40 mph for 1.5 hours, what's the average speed?"
2. Send query: "Analyze the pros and cons of renewable energy adoption"
**Expected Result**: Step-by-step solution showing reasoning process
**Pass Criteria**: Clear logical progression, correct final answers

### Test Case 3.2: Analytical Reasoning
**Objective**: Verify Reasoning Agent can perform analysis and draw conclusions
**Steps**:
1. Send query: "What would be the impact of a 4-day work week on productivity?"
2. Send query: "Should a startup prioritize growth or profitability first?"
**Expected Result**: Structured analysis with multiple perspectives and reasoned conclusions
**Pass Criteria**: Logical analysis, consideration of multiple factors

## Memory Agent Tests

### Test Case 4.1: Personal Information Storage
**Objective**: Verify Memory Agent can store and retrieve personal information
**Steps**:
1. Send query: "Remember that my favorite color is blue and I live in Seattle"
2. Later send query: "What's my favorite color?"
3. Send query: "Where do I live?"
**Expected Result**: Agent stores information and retrieves it accurately later
**Pass Criteria**: Information persisted correctly, accurate retrieval

### Test Case 4.2: Vector Similarity Matching
**Objective**: Verify Memory Agent uses vector similarity for related information retrieval
**Steps**:
1. Store information: "I work as a software engineer at Microsoft"
2. Store information: "My hobby is playing guitar and I love jazz music"
3. Send query: "Tell me about my professional background"
**Expected Result**: Agent retrieves related professional information using similarity matching
**Pass Criteria**: Relevant information retrieved, similarity matching works correctly

## RAG Agent Tests

### Test Case 5.1: Knowledge Base Retrieval
**Objective**: Verify RAG Agent can retrieve information from knowledge base using TF-IDF
**Steps**:
1. Ensure knowledge base is populated with documents
2. Send query: "Find information about machine learning algorithms"
3. Send query: "What does the knowledge base say about neural networks?"
**Expected Result**: Relevant documents retrieved and synthesized into coherent response
**Pass Criteria**: Accurate retrieval, proper TF-IDF ranking, coherent synthesis

### Test Case 5.2: TF-IDF Vectorization Accuracy
**Objective**: Verify vectorization works correctly for document ranking
**Steps**:
1. Add documents with varying relevance to a specific topic
2. Send query about that topic
3. Verify most relevant documents are ranked highest
**Expected Result**: Documents ranked by relevance, most relevant content prioritized
**Pass Criteria**: Proper scoring, accurate relevance ranking

## Team Agent Tests

### Test Case 3.1: Correct Agent Routing
**Objective**: Verify Team Agent routes queries to appropriate specialized agents
**Steps**:
1. Send mathematical query (should route to Direct Agent)
2. Send complex explanation request (should route to Knowledge Agent)
3. Send multi-step problem (should route to Reasoning Agent)
4. Send personal information query (should route to Memory Agent)
**Expected Result**: Each query routed to the correct specialized agent
**Pass Criteria**: 100% routing accuracy, appropriate agent handles each query type

### Test Case 6.2: Routing Decision Logging
**Objective**: Verify routing decisions are logged and trackable
**Steps**:
1. Send various types of queries
2. Check system logs for routing decisions
3. Verify routing rationale is recorded
**Expected Result**: All routing decisions logged with reasoning
**Pass Criteria**: Complete routing logs, clear decision rationale