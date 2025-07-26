# Getting Started

OnCallM is an AI-powered Kubernetes alert analysis tool that helps DevOps teams reduce Mean Time To Resolution (MTTR) by providing intelligent root cause detection and actionable insights.

## What is OnCallM?

OnCallM analyzes Kubernetes alerts from AlertManager and uses AI to:

- **Identify root causes** automatically by analyzing logs, metrics, and cluster state
- **Provide actionable recommendations** with specific steps to resolve issues
- **Reduce alert fatigue** by providing intelligent summaries and prioritized action items
- **Accelerate incident response** with detailed analysis reports in seconds

## Key Benefits

::: tip ⚡ 80% Faster Resolution
OnCallM's AI-powered analysis helps teams resolve incidents 80% faster than traditional manual approaches.
:::

::: tip 🧠 Intelligent Analysis
Advanced AI understands Kubernetes environments and provides context-aware insights.
:::

::: tip 🔄 Easy Integration
Simple webhook integration with AlertManager - deploy once and start getting insights immediately.
:::

## How It Works

1. **Alert Integration**: OnCallM receives alerts from your AlertManager via webhook
2. **AI Analysis**: Our AI analyzes alert context, logs, metrics, and cluster state
3. **Actionable Insights**: Receive detailed reports with specific recommendations

## Quick Start

Ready to get started? Follow our [deployment guide](../deployment/quick-start.md) to set up OnCallM in your Kubernetes cluster.

## Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   AlertManager  │───▶│     OnCallM     │───▶│   AI Analysis   │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Kubernetes     │◀───│  Data Collection│    │ Analysis Report │
│  Cluster        │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Next Steps

- [Learn how OnCallM works](./how-it-works.md)
- [Explore features](./features.md)
- [Deploy OnCallM](../deployment/quick-start.md)
- [Configure AlertManager](../configuration/alertmanager.md) 