
import unittest

from lib.utils import get_smk_file

class TestGetSmkFile(unittest.TestCase):

    def test_rna_fullanalysis(self):
        """Test RNA pipeline with full analysis"""
        result = get_smk_file("rna", fullanalysis=True)
        self.assertEqual(result, "workflow/Snakefile_rna_fullanalysis")

    def test_rna_no_fullanalysis(self):
        """Test RNA pipeline without full analysis"""
        result = get_smk_file("rna", fullanalysis=False)
        self.assertEqual(result, "workflow/Snakefile_rna")

    def test_multi_pipeline(self):
        """Test multi pipeline"""
        result = get_smk_file("multi")
        self.assertEqual(result, "workflow/Snakefile_multi")

    def test_vdj_pipeline(self):
        """Test VDJ pipeline"""
        result = get_smk_file("vdj")
        self.assertEqual(result, "workflow/Snakefile_vdj")

    def test_spatial_pipeline(self):
        """Test spatial pipeline"""
        result = get_smk_file("spatial")
        self.assertEqual(result, "workflow/Snakefile_spatial")

    def test_invalid_pipeline(self):
        """Test an invalid pipeline that should return None"""
        result = get_smk_file("invalid")
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()

