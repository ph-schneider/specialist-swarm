---
name: technical-fit
description: BTS-Synthetic capability map and fit-assessment method for the Technical Fit Specialist. Use whenever assessing whether our product covers the RFP's technical requirements — workloads, scale, architecture, governance, SLAs, compliance, implementation timeline. Produces a structured fit assessment with honest full / partial / no-fit calls.
---

# Technical Fit Assessment

Use this when the coordinator asks whether our product covers the RFP's requirements.

## Method

1. **Extract the technical requirements** from the RFP: workloads, scale/volume,
   capabilities, architecture, governance, compliance, SLAs, and implementation
   timeline. Commercial terms (pricing, discounts, MFN, termination) and
   legal clauses (liability, audit, IP, subprocessors) are NOT your lane —
   leave those to the pricing and legal specialists.
2. **Rate each requirement** against the capability map below:
   - **Full fit** — covered natively, out of the box.
   - **Partial fit** — we can deliver it, but with a caveat, custom add-on,
     workaround, or bespoke architecture. Say exactly what's missing or
     what it costs to close the gap.
   - **No fit** — we can't do it. Say so plainly; never paper over it.
3. **Be honest.** The "Where we're weak" section below is there to be used.
   A partial fit that surfaces early costs us credibility, not the deal.
   A full fit we can't deliver costs us the deal.
4. **Respect the RFP's own stakes.** If the RFP marks a requirement as
   non-negotiable or a must-have, call it out explicitly in the risk section,
   even if you rate it a fit.
5. **Don't invent requirements.** Where the RFP is silent, don't speculate;
   list your assumptions separately.

## Capability map

### Core architecture
- Lakehouse with native support for Delta, Iceberg, and Parquet file formats.
- Object storage backend — bring-your-own S3, Azure Blob, or GCS.
- Compute decoupled from storage. Multiple compute engines: SQL,
  Spark-equivalent, streaming.
- Multi-cloud: deployable on AWS, Azure, GCP. Multi-region within each cloud.
- Self-hosted option for sovereignty-sensitive customers.

### Ingest
- Batch ETL: 80+ connectors out of the box (Salesforce, SAP, NetSuite,
  common databases).
- Real-time streaming: native Kafka and Kinesis consumers. Tested up to
  250K events/second on single-region deployments.
- CDC (change data capture) from major databases via
  Debezium-compatible connectors.

### Analytics
- SQL workloads: full ANSI SQL, sub-second on warmed caches up to 10TB.
- Notebooks for data scientists: Python, R, Scala.
- BI integrations: certified integrations with Power BI, Tableau, Looker,
  Qlik. Power BI is our most mature BI integration (dedicated DirectQuery
  adapter).
- Self-service prep: low-code data prep UI for analyst personas.

### Governance
- Unity-style catalog for tables, models, dashboards.
- Row-level + column-level security with attribute-based access control.
- Data residency: per-table residency enforcement. EU data tables can be
  pinned to EU regions.
- Audit logs: every read and write logged, exportable to customer SIEM.
- PII detection and masking built-in.

### ML / AI
- Model registry with versioning.
- Feature store for offline + online serving.
- Native model serving with autoscaling.
- Bring-your-own-model: any HuggingFace, Anthropic, or OpenAI model can be
  called from within the platform.

### SLA
- 99.95% monthly uptime on Enterprise tier.
- 99.99% available as a custom add-on with bespoke architecture —
  typically $80K–$120K/year premium and requires multi-region active-active.

### Compliance
- SOC 2 Type II
- ISO 27001
- HIPAA-eligible
- GDPR-aligned (DPA available)
- FedRAMP Moderate (US Gov tier only)

## Where we're WEAK

Important honest list — use this when assessing fit:
- **Real-time analytics at sub-100ms latency**: we're not best-in-class here.
  We hit ~250ms–1s on streaming queries. If the RFP demands sub-100ms,
  flag as partial fit.
- **Geospatial workloads**: basic support only, no advanced geospatial
  indexing.
- **Graph workloads**: not natively supported. Customers do this in separate
  graph databases.
- **No native Power Apps connector** (Power BI yes, Power Apps no —
  customers usually OK with this).

## Rating guidance (frequently contested items)

| RFP asks for | Rating | Note |
| --- | --- | --- |
| Sub-100ms streaming analytics | Partial | We're at ~250ms–1s |
| 99.99% uptime SLA | Partial | Custom add-on, multi-region active-active, $80K–$120K/yr premium — flag the cost |
| 99.95% uptime SLA | Full | Enterprise tier standard |
| Power BI integration | Full | Most mature BI integration (DirectQuery adapter) |
| Power Apps connector | No fit | No native connector; customer usually accepts |
| Graph workloads | No fit | Not native |
| Geospatial | Partial | Basic only |
| Multi-region + EU data residency | Full | Per-table residency, EU pinning |
| Lakehouse / open formats (Delta, Iceberg, Parquet) | Full | Native |
| Migration off Teradata/Hadoop | Full, but plan for ~16 weeks | 8 weeks if clean source systems; 24 weeks for very large multi-region |

## Implementation timeline (typical)
- **8 weeks** to first production workload for a customer with clean
  source systems.
- **16 weeks** for full migration from legacy warehouse like Teradata
  or Hadoop.
- **24 weeks** for very large, multi-region, multi-source customers.

Use these when the RFP has an implementation timeline criterion or asks
for go-live dates — quote them honestly, don't compress them.

## Output format

1. Requirements we meet fully (one line each, with the capability that covers it)
2. Requirements we meet partially (and exactly what's missing or what it takes to close the gap)
3. Requirements we don't meet at all (flag honestly)
4. Overall fit score: high / medium / low
5. The single most important risk to flag to the coordinator
