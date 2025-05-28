# DevOps Prioritization Scenarios – Q&A

---

## Q1: Onboarding a New Microservice in Kubernetes – What to Automate First?

**Ranking:**

1. **CI/CD pipeline to deploy new images to Kubernetes**  
   _Why_: Automating deployments ensures fast and repeatable releases. Once manifests exist, integrating them into CI/CD is the next priority.

2. **Monitoring and alerting (Prometheus + Grafana)**  
   _Why_: Observability is crucial to identify failures or performance issues early in production.

3. **Helm/Kustomize templates for Kubernetes manifests**  
   _Why_: Foundational for deployment. Brings reusability and consistency.

4. **GitHub Actions for tests and quality checks**  
   _Why_: Valuable for early feedback, but secondary to base deployment automation.

5. **Documentation in Confluence or a runbook**  
   _Why_: Important, but lower priority than automation and observability.

---

## Q2: Most Important Automation in a High-Scale Environment?

**Ranking:**

1. **CI/CD deployments (build → test → release)**  
   _Why_: Ensures velocity, consistency, and reduces human error.

2. **Security patching and base image updates**  
   _Why_: Reduces vulnerabilities at scale.

3. **Log rotation and archival**  
   _Why_: Important but lower urgency than uptime/security-impacting tasks.

4. **Instance scaling and load balancing**  
   _Why_: Critical for managing traffic efficiently.

5. **Incident response and alert escalation**  
   _Why_: Some parts can be automated (e.g., paging), but human judgment is often needed.

---

## Q3: Fixing Slow Manual Deployments – What to Implement First?

**Ranking:**

1. **CI pipelines for automated deployments (Jenkins/GitLab)**  
   _Why_: Fixes the root cause — slow, error-prone manual deployments.

2. **Monitoring & alerting**  
   _Why_: Ensures visibility once deployments are automated.

3. **Terraform/CloudFormation for infrastructure provisioning**  
   _Why_: Provides consistency and makes scaling infra easier.

4. **Centralized logging (Elasticsearch or Loki)**  
   _Why_: Useful for debugging, but comes after deployment reliability.

5. **Canary deployments with rollback**  
   _Why_: Advanced strategy; comes after core systems are in place.

---

## Q4: During an Incident – What to Investigate First?

**Ranking:**

1. **Recent code/config changes**  
   _Why_: Most incidents stem from recent changes.

2. **Alert/log timestamps**  
   _Why_: Helps correlate timing and locate the root cause quickly.

3. **Resource metrics (CPU, memory, disk)**  
   _Why_: Identifies system-level performance issues.

4. **Network traffic/service dependencies**  
   _Why_: Slower to investigate unless the issue is clearly networking-related.

5. **Kubernetes pod restarts/crash loops**  
   _Why_: Often a symptom of deeper issues.

---

## Q5: Migrating from VMs to Containers – What Comes First?

**Recommended Order:**

1. **Implement Terraform for Infrastructure as Code**  
   _Why_: Standardizes environments before deploying containers.

2. **Migrate apps to Docker and container registries**  
   _Why_: Core step in transitioning to containers.

3. **Build CI pipelines for container images**  
   _Why_: Enables consistent testing and delivery of Dockerized apps.

4. **Deploy apps to Kubernetes using Helm**  
   _Why_: Adds orchestration and scalability.

5. **Set up observability stack (Prometheus, Grafana, Loki)**  
   _Why_: Monitoring becomes essential once apps are running.

---

## Q6: Reducing Manual Work in the Release Process – What to Automate?

**Recommended Order:**

1. **Build and test on code push**  
   _Why_: Enables fast feedback and prevents bad code early.

2. **Deploy to staging with rollback support**  
   _Why_: Validates changes in a pre-prod environment safely.

3. **Change management gates/approvals**  
   _Why_: Maintains compliance without slowing down delivery.

4. **Deploy to production with health checks**  
   _Why_: Must be safe, observable, and automatic.

5. **Update monitoring dashboards**  
   _Why_: Nice to have early on but not critical to core release automation.

---

## Q7: Signals of Poor Automation Maturity

**Ranking:**

1. **Infra changes without PRs or peer review**  
   _Why_: Zero accountability, high risk, and non-collaborative culture.

2. **Manual infra provisioning in AWS Console**  
   _Why_: Bypasses IaC, making infra inconsistent and error-prone.

3. **Logs stored on ephemeral disks**  
   _Why_: Impacts debugging but not core automation.

4. **No alerting for failed deployments**  
   _Why_: Erodes trust in pipelines; delays incident response.

5. **Manual rollback steps during release**  
   _Why_: Risky but sometimes needed in edge cases; should be automated.

---

