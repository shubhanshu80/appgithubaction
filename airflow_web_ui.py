#!/usr/bin/env python3
"""
Simple ML Pipeline Web UI - Airflow-like interface
"""

from flask import Flask, render_template_string
import json
from datetime import datetime

app = Flask(__name__)

# DAG configuration
DAG_CONFIG = {
    'dag_id': 'ml_pipeline_dag',
    'owner': 'ml-team',
    'description': 'ML CI/CD Pipeline with Data Processing and Model Training',
    'schedule': '0 2 * * *',
    'tasks': {
        'fetch_data': {
            'description': 'Fetch data from source',
            'depends_on': [],
            'color': '#4CAF50',
            'status': 'success'
        },
        'validate_data': {
            'description': 'Validate fetched data quality',
            'depends_on': ['fetch_data'],
            'color': '#2196F3',
            'status': 'success'
        },
        'preprocess_data': {
            'description': 'Clean and preprocess data',
            'depends_on': ['validate_data'],
            'color': '#FF9800',
            'status': 'success'
        },
        'train_model': {
            'description': 'Train ML model',
            'depends_on': ['preprocess_data'],
            'color': '#9C27B0',
            'status': 'success'
        },
        'evaluate_model': {
            'description': 'Evaluate model performance',
            'depends_on': ['train_model'],
            'color': '#F44336',
            'status': 'success'
        },
        'run_tests': {
            'description': 'Run unit tests',
            'depends_on': ['train_model'],
            'color': '#00BCD4',
            'status': 'success'
        },
        'deploy_model': {
            'description': 'Deploy to production',
            'depends_on': ['evaluate_model', 'run_tests'],
            'color': '#8BC34A',
            'status': 'success'
        },
        'log_results': {
            'description': 'Log final results',
            'depends_on': ['deploy_model'],
            'color': '#607D8B',
            'status': 'success'
        }
    }
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Airflow - ML Pipeline</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: #f5f5f5;
        }
        
        .navbar {
            background: #003f5c;
            color: white;
            padding: 0 20px;
            height: 60px;
            display: flex;
            align-items: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .navbar svg {
            width: 40px;
            height: 40px;
            margin-right: 15px;
        }
        
        .navbar h1 {
            font-size: 1.5em;
            margin: 0;
        }
        
        .container {
            max-width: 1400px;
            margin: 20px auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
        }
        
        .header h2 {
            font-size: 2em;
            margin-bottom: 10px;
        }
        
        .header p {
            opacity: 0.9;
            font-size: 1em;
        }
        
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }
        
        .info-item {
            background: rgba(255,255,255,0.1);
            padding: 10px 15px;
            border-radius: 6px;
        }
        
        .info-item label {
            display: block;
            font-size: 0.8em;
            opacity: 0.8;
            margin-bottom: 5px;
        }
        
        .info-item value {
            display: block;
            font-size: 1.1em;
            font-weight: bold;
        }
        
        .content {
            padding: 30px;
        }
        
        .section-title {
            font-size: 1.5em;
            color: #333;
            margin-bottom: 20px;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }
        
        #graph-container {
            background: #f9f9f9;
            border: 2px dashed #ddd;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 30px;
            min-height: 500px;
        }
        
        svg {
            width: 100%;
            height: auto;
        }
        
        .task-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        
        .task-card {
            border: 1px solid #ddd;
            border-radius: 6px;
            padding: 15px;
            background: white;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .task-card:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            transform: translateY(-2px);
        }
        
        .task-header {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 10px;
        }
        
        .task-status {
            width: 16px;
            height: 16px;
            border-radius: 50%;
            flex-shrink: 0;
        }
        
        .task-name {
            font-weight: bold;
            font-size: 1.1em;
            color: #333;
        }
        
        .task-description {
            font-size: 0.9em;
            color: #666;
            margin-bottom: 10px;
        }
        
        .status-badge {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.85em;
            font-weight: bold;
            background: #4CAF50;
            color: white;
        }
        
        .footer {
            background: #f5f5f5;
            padding: 20px;
            text-align: center;
            color: #666;
            border-top: 1px solid #ddd;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="navbar">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2m0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8"/>
        </svg>
        <h1>Airflow</h1>
    </div>
    
    <div class="container">
        <div class="header">
            <h2>{{ dag_id }}</h2>
            <p>{{ description }}</p>
            <div class="info-grid">
                <div class="info-item">
                    <label>Owner</label>
                    <value>{{ owner }}</value>
                </div>
                <div class="info-item">
                    <label>Schedule</label>
                    <value>{{ schedule }}</value>
                </div>
                <div class="info-item">
                    <label>Tasks</label>
                    <value>{{ task_count }}</value>
                </div>
                <div class="info-item">
                    <label>Last Run</label>
                    <value>{{ last_run }}</value>
                </div>
            </div>
        </div>
        
        <div class="content">
            <h2 class="section-title">📊 DAG Graph</h2>
            <div id="graph-container">
                <svg id="dag-svg"></svg>
            </div>
            
            <h2 class="section-title">📋 Tasks</h2>
            <div class="task-grid" id="task-grid"></div>
        </div>
        
        <div class="footer">
            <p>Generated on {{ timestamp }} • Airflow Version 2.5.3</p>
        </div>
    </div>
    
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <script>
        const tasks = {{ tasks_json | safe }};
        const taskIds = Object.keys(tasks);
        
        // Generate task cards
        const taskGrid = document.getElementById('task-grid');
        taskIds.forEach(taskId => {
            const task = tasks[taskId];
            const card = document.createElement('div');
            card.className = 'task-card';
            const depsText = task.depends_on.length > 0 ? task.depends_on.join(', ') : 'None';
            card.innerHTML = `
                <div class="task-header">
                    <div class="task-status" style="background-color: ${task.color}"></div>
                    <div class="task-name">${taskId.replace(/_/g, ' ').toUpperCase()}</div>
                </div>
                <p class="task-description">${task.description}</p>
                <div><strong>Depends on:</strong> ${depsText}</div>
                <div style="margin-top: 10px;">
                    <span class="status-badge">${task.status.toUpperCase()}</span>
                </div>
            `;
            taskGrid.appendChild(card);
        });
        
        // Create DAG visualization
        const svg = d3.select("#dag-svg");
        const width = document.getElementById("graph-container").clientWidth;
        const height = 500;
        
        svg.attr("width", width).attr("height", height);
        
        // Add arrow marker
        svg.append("defs").append("marker")
            .attr("id", "arrowhead")
            .attr("markerWidth", 10)
            .attr("markerHeight", 10)
            .attr("refX", 9)
            .attr("refY", 3)
            .attr("orient", "auto")
            .append("polygon")
            .attr("points", "0 0, 10 3, 0 6")
            .attr("fill", "#999");
        
        // Position nodes
        const positionMap = {
            'fetch_data': [100, 100],
            'validate_data': [100, 200],
            'preprocess_data': [100, 300],
            'train_model': [100, 400],
            'evaluate_model': [300, 400],
            'run_tests': [500, 400],
            'deploy_model': [400, 450],
            'log_results': [400, 550]
        };
        
        // Create links
        const links = [];
        taskIds.forEach(taskId => {
            const task = tasks[taskId];
            task.depends_on.forEach(dep => {
                links.push({
                    source: positionMap[dep],
                    target: positionMap[taskId]
                });
            });
        });
        
        svg.selectAll(".link")
            .data(links)
            .enter()
            .append("line")
            .attr("x1", d => d.source[0])
            .attr("y1", d => d.source[1])
            .attr("x2", d => d.target[0])
            .attr("y2", d => d.target[1])
            .attr("stroke", "#999")
            .attr("stroke-width", 2)
            .attr("marker-end", "url(#arrowhead)");
        
        // Create nodes
        svg.selectAll(".node")
            .data(taskIds)
            .enter()
            .append("circle")
            .attr("cx", d => positionMap[d][0])
            .attr("cy", d => positionMap[d][1])
            .attr("r", 40)
            .attr("fill", d => tasks[d].color)
            .attr("stroke", "#333")
            .attr("stroke-width", 2);
        
        // Add labels
        svg.selectAll(".node-label")
            .data(taskIds)
            .enter()
            .append("text")
            .attr("x", d => positionMap[d][0])
            .attr("y", d => positionMap[d][1])
            .attr("text-anchor", "middle")
            .attr("dominant-baseline", "middle")
            .attr("fill", "white")
            .attr("font-size", "12px")
            .attr("font-weight", "bold")
            .attr("pointer-events", "none")
            .text(d => d.replace(/_/g, '\\n'));
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(
        HTML_TEMPLATE,
        dag_id=DAG_CONFIG['dag_id'],
        owner=DAG_CONFIG['owner'],
        description=DAG_CONFIG['description'],
        schedule=DAG_CONFIG['schedule'],
        task_count=len(DAG_CONFIG['tasks']),
        last_run=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        tasks_json=json.dumps(DAG_CONFIG['tasks'])
    )

if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════════════╗
    ║   🚀 ML Pipeline Airflow-like Web UI            ║
    ║                                                ║
    ║   Open your browser at:                       ║
    ║   👉  http://localhost:5000                   ║
    ║                                                ║
    ║   Press Ctrl+C to stop the server             ║
    ╚════════════════════════════════════════════════╝
    """)
    app.run(debug=True, port=5000, use_reloader=False)
