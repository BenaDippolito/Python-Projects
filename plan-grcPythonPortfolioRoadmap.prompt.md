## GRC Python Portfolio Roadmap

You have a strong starting point with Python, cybersecurity knowledge, and the ISC2 CGRC certification. These projects are ordered by direct GRC relevance and portfolio value.

### 1. GRC Control and Evidence Tracker

Build a system for tracking controls, control owners, implementation status, evidence, review dates, and findings.

Steps:

1. Define control fields and statuses.
2. Map controls to NIST CSF, NIST 800-53, CIS Controls, or ISO 27001.
3. Create a SQLite or JSON data model.
4. Add evidence upload or evidence-link tracking.
5. Implement review dates and overdue controls.
6. Add filtering and reporting.
7. Write tests and document the workflow.
8. Produce a sample assessment using fictional data.

**Best starting project.**

### 2. Enterprise Risk Register

Create a risk management application for identifying, scoring, treating, and monitoring organizational risks.

Steps:

1. Define risk categories and scoring criteria.
2. Implement likelihood, impact, and inherent-risk calculations.
3. Add treatment plans, owners, due dates, and residual risk.
4. Add risk acceptance and escalation statuses.
5. Create risk heat-map reporting.
6. Add overdue-risk detection.
7. Write tests for scoring and status transitions.
8. Document the risk methodology.

### 3. Third-Party Vendor Risk Assessment Tool

Build a questionnaire and scoring workflow for evaluating suppliers and service providers.

Steps:

1. Define vendor profiles and criticality levels.
2. Create assessment questions by domain.
3. Implement weighted scoring.
4. Track evidence and remediation items.
5. Add approval and review workflows.
6. Generate vendor risk reports.
7. Add reassessment scheduling.
8. Document how the tool supports vendor due diligence.

### 4. Security Policy Compliance Checker

Create a tool that evaluates configuration or evidence against organizational policy requirements.

Possible areas include password policy, encryption, backups, access control, or logging.

Steps:

1. Choose one policy domain.
2. Translate policy language into testable requirements.
3. Define input evidence formats.
4. Implement pass, fail, and not-applicable results.
5. Add exceptions and compensating controls.
6. Generate an executive summary.
7. Test both compliant and noncompliant cases.
8. Document assumptions and limitations.

### 5. Audit Evidence Collection and Reporting Tool

Build a workflow for collecting evidence during internal audits or compliance assessments.

Steps:

1. Define audit scope, objectives, and control population.
2. Create evidence-request records.
3. Track owners, due dates, status, and reviewer comments.
4. Add evidence validation and approval states.
5. Track gaps and follow-up actions.
6. Generate an audit-readiness report.
7. Add audit-trail logging.
8. Document the evidence lifecycle.

### 6. IT Asset Inventory and Data Classification Tool

Create an inventory system for systems, applications, data stores, owners, classifications, and criticality.

Steps:

1. Define asset categories and required metadata.
2. Add confidentiality, integrity, and availability ratings.
3. Implement data classification levels.
4. Track asset owners and business functions.
5. Add lifecycle and review statuses.
6. Identify assets missing required information.
7. Generate inventory and classification reports.
8. Use entirely synthetic sample data.

### 7. Access Review and User Entitlement Analyzer

Build a tool that supports periodic access certifications and identifies excessive or conflicting access.

Steps:

1. Define users, roles, systems, and entitlements.
2. Import sample access data from CSV.
3. Detect inactive users and stale access.
4. Identify privileged accounts.
5. Add basic segregation-of-duties rules.
6. Track reviewer decisions and exceptions.
7. Generate access-review reports.
8. Document privacy and data-minimization controls.

### 8. Security Incident and Corrective Action Tracker

Create a GRC-focused incident workflow that tracks incidents, root causes, corrective actions, and lessons learned.

Steps:

1. Define incident categories and severity levels.
2. Create incident intake fields.
3. Track affected assets and business impact.
4. Add root-cause and contributing-factor fields.
5. Create corrective and preventive actions.
6. Track owners and deadlines.
7. Generate trend and overdue-action reports.
8. Document that the tool is for governance tracking, not a replacement for a SIEM or SOC platform.

### 9. Business Continuity and Disaster Recovery Assessment Tool

Build a tool for tracking business processes, recovery requirements, dependencies, and test results.

Steps:

1. Define business processes and criticality.
2. Track RTO and RPO requirements.
3. Record system and vendor dependencies.
4. Add recovery-plan status.
5. Track continuity exercises and test outcomes.
6. Record findings and remediation actions.
7. Generate readiness reports.
8. Use fictional organizational data and clearly state assumptions.

### 10. Compliance Obligation and Regulatory Change Tracker

Create a system for tracking obligations, requirements, applicability, owners, and implementation status.

Steps:

1. Choose a limited example scope, such as NIST, SOC 2, or ISO 27001.
2. Define obligations and requirement metadata.
3. Track applicability decisions.
4. Map obligations to controls and policies.
5. Add owners, deadlines, and review dates.
6. Track regulatory-change records manually using sample data.
7. Generate an obligation-status report.
8. Document that the tool does not provide legal advice.

## Recommended Order

1. GRC Control and Evidence Tracker  
2. Enterprise Risk Register  
3. Third-Party Vendor Risk Assessment Tool  
4. Audit Evidence Collection Tool  
5. Access Review Analyzer  
6. Security Policy Compliance Checker  
7. Asset Inventory Tool  
8. Incident Corrective Action Tracker  
9. Business Continuity Assessment Tool  
10. Compliance Obligation Tracker  

## Git Workflow

Once you select a project, I will advise you to create Git checkpoints at these stages:

- Initial project structure
- First working vertical slice
- Core feature completion
- Tests and validation
- Documentation and sample data
- Portfolio-ready release

I will provide the exact `git add`, `git commit`, and `git push` commands, but you will execute them through the terminal.

No project files have been modified. Select a project by number, with **1** recommended as the best first portfolio project.
