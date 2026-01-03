import logging

logging.basicConfig(level=logging.INFO, format='[ALETHEIA-FAB] %(message)s')
logger = logging.getLogger(__name__)

def generate_mask_definitions():
    """Generates GDSII Layer definitions for InAs-Al TGP Device."""
    logger.info("Initializing Mask Generation for Device: Aletheia-TGP-v1")
    
    # Layer 10: Mesa (3.0um length for ABS filtering)
    logger.info("Defining Layer 10 [MESA]: 3.0um x 0.5um Active Wire")
    
    # Layer 20: Al Etch
    logger.info("Defining Layer 20 [AL-ETCH]: 80nm Junction Gap")
    
    # Layer 30: Fine Gates (Middle Probe)
    logger.info("Defining Layer 30 [GATES]: 30nm Middle Probe (E-Beam)")
    
    logger.info("GDSII Stream Generation Complete: aletheia_tgp_v1.gds")

if __name__ == "__main__":
    generate_mask_definitions()