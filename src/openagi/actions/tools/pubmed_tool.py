from openagi.actions.base import ConfigurableAction
from openagi.exception import OpenAGIException
from pydantic import Field

try:
	from Bio import Entrez
except ImportError:
	raise OpenAGIException("Install Biopython with cmd `pip install biopython`")

class PubMedSearch(ConfigurableAction):
	"""PubMed Search tool for querying biomedical literature.
	
	This action uses the Bio.Entrez module to search PubMed and retrieve
	scientific articles based on user queries. Requires an email address
	to be configured for NCBI's tracking purposes.
	"""
	
	query: str = Field(..., description="Search query for PubMed")
	max_results: int = Field(
		default=5,
		description="Maximum number of results to return (default: 5)"
	)
	sort: str = Field(
		default="relevance",
		description="Sort order: 'relevance', 'pub_date', or 'first_author'"
	)

	def execute(self) -> str:
		email: str = self.get_config('email')
		if not email:
			raise OpenAGIException(
				"Email not configured. Use PubMedSearch.set_config(email='your_email@example.com')"
			)

		Entrez.email = email
		
		try:
			# Search PubMed
			search_handle = Entrez.esearch(
				db="pubmed",
				term=self.query,
				retmax=self.max_results,
				sort=self.sort
			)
			search_results = Entrez.read(search_handle)
			search_handle.close()

			if not search_results["IdList"]:
				return "No results found for the given query."

			# Fetch details for found articles
			ids = ",".join(search_results["IdList"])
			fetch_handle = Entrez.efetch(
				db="pubmed",
				id=ids,
				rettype="medline",
				retmode="text"
			)
			
			results = fetch_handle.read()
			fetch_handle.close()

			# Process and format results
			formatted_results = (
				f"Found {len(search_results['IdList'])} results for query: {self.query}\n\n"
				f"{results}"
			)

			return formatted_results

		except Exception as e:
			return f"Error searching PubMed: {str(e)}"