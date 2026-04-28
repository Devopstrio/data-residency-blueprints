import logging
import uuid
import time

class ResidencyPolicyEngine:
    def __init__(self):
        self.logger = logging.getLogger("residency-policy")

    def calculate_compliance_score(self, region_id: str, checks: list):
        """
        Aggregates individual residency checks into a regional compliance score.
        """
        if not checks:
            return 1.0
        
        passed_count = sum(1 for c in checks if c["passed"])
        score = passed_count / len(checks)
        return round(score, 4)

    def validate_region_placement(self, resource_type: str, current_region: str, allowed_regions: list):
        """
        Validates if a specific resource is placed in an allowed sovereign region.
        """
        is_allowed = current_region in allowed_regions
        self.logger.info(f"Validating placement for {resource_type}: {current_region} -> Allowed: {is_allowed}")
        
        return {
            "is_valid": is_allowed,
            "resource_type": resource_type,
            "region": current_region,
            "violation": None if is_allowed else "UNAUTHORIZED_REGION_PLACEMENT"
        }

    def evaluate_transfer_risk(self, source_region: str, target_region: str, data_sensitivity: str):
        """
        Scores the risk of a cross-border data transfer.
        """
        # Logic: Cross-continent transfers are higher risk
        risk_level = "LOW"
        if source_region[:2] != target_region[:2]:
            risk_level = "HIGH" if data_sensitivity == "CRITICAL" else "MEDIUM"
            
        return {
            "risk_level": risk_level,
            "source": source_region,
            "target": target_region,
            "requires_dpo_approval": risk_level != "LOW"
        }

    def check_encryption_locality(self, key_urn: str, region_id: str):
        """
        Ensures encryption keys are pinned to the correct regional HSM.
        """
        # Simulated check: URN should contain the regional code
        is_local = region_id.lower() in key_urn.lower()
        return {
            "is_local": is_local,
            "key_urn": key_urn,
            "region_id": region_id
        }

if __name__ == "__main__":
    engine = ResidencyPolicyEngine()
    
    # 1. Placement Validation
    print("Placement Check:", engine.validate_region_placement("SQL_DB", "us-east-1", ["eu-west-1", "eu-central-1"]))
    
    # 2. Transfer Risk
    print("Transfer Risk:", engine.evaluate_transfer_risk("eu-west-1", "us-east-1", "CRITICAL"))
    
    # 3. Compliance Score
    checks = [{"passed": True}, {"passed": False}, {"passed": True}]
    print("Regional Score:", engine.calculate_compliance_score("eu-boundary", checks))
    
    # 4. Key Locality
    print("Key Locality:", engine.check_encryption_locality("arn:aws:kms:eu-west-1:123:key/abc", "eu-west-1"))
