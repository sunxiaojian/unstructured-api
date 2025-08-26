from typing import Annotated, List, Literal, Optional, Any

from fastapi import Form, Request
from pydantic import BaseModel, BeforeValidator

from prepline_general.api.utils import SmartValueParser


class GeneralFormParams(BaseModel):
    """
    Form parameters for the General Partition API.
    Add new parameters here and in the as_form classmethod.
    Use Annotated to provide descriptions and examples.
    """

    xml_keep_tags: bool
    languages: Optional[List[str]]
    ocr_languages: Optional[List[str]]
    skip_infer_table_types: Optional[List[str]]
    gz_uncompressed_content_type: Optional[str]
    output_format: str
    coordinates: bool
    encoding: str
    content_type: Optional[str]
    hi_res_model_name: Optional[str]
    include_page_breaks: bool
    pdf_infer_table_structure: bool
    strategy: str
    extract_image_block_types: Optional[List[str]]
    unique_element_ids: bool
    starting_page_number: Optional[int] = None
    include_slide_notes: bool
    # Chunking options
    chunking_strategy: Optional[str]
    combine_under_n_chars: Optional[int]
    max_characters: int
    multipage_sections: bool
    new_after_n_chars: Optional[int]
    overlap: int
    overlap_all: bool
    splitter_kwargs: Optional[dict[str, Any]] = None

    @classmethod
    async def as_form(
        cls,
        request: Request,
        xml_keep_tags: Annotated[
            bool,
            Form(
                title="XML Keep Tags",
                description="Retain XML tags in output (only for partition_xml)",
            ),
            BeforeValidator(SmartValueParser[bool]().value_or_first_element),
        ] = False,
        languages: Annotated[
            List[str],
            Form(
                title="OCR Languages",
                description="Languages for partitioning/OCR",
                examples=["[eng]"],
            ),
            BeforeValidator(SmartValueParser[List[str]]().value_or_first_element),
        ] = [],  # noqa
        ocr_languages: Annotated[
            List[str],
            Form(
                title="OCR Languages",
                description="Languages for partitioning/OCR",
                examples=["[eng]"],
            ),
            BeforeValidator(SmartValueParser[List[str]]().value_or_first_element),
        ] = [],
        skip_infer_table_types: Annotated[
            List[str],
            Form(
                title="Skip Table Extraction",
                description="Document types to skip table extraction",
                examples=["['pdf', 'jpg', 'png']"],
            ),
            BeforeValidator(SmartValueParser[List[str]]().value_or_first_element),
        ] = [],  # noqa
        gz_uncompressed_content_type: Annotated[
            Optional[str],
            Form(
                title="Uncompressed Content Type",
                description="Content type after unzipping gzipped files",
                examples=["application/pdf"],
            ),
        ] = None,
        output_format: Annotated[
            Literal["application/json", "text/csv"],
            Form(
                title="Output Format",
                description="Response format (application/json or text/csv)",
                examples=["application/json"],
            ),
        ] = "application/json",
        coordinates: Annotated[
            bool,
            Form(
                title="Coordinates",
                description="Return element coordinates",
            ),
            BeforeValidator(SmartValueParser[bool]().value_or_first_element),
        ] = False,
        content_type: Annotated[
            Optional[str],
            Form(
                title="Content Type Hint",
                description="MIME type hint for problematic files",
                examples=["text/markdown"],
            ),
            BeforeValidator(SmartValueParser[str]().value_or_first_element),
        ] = None,
        encoding: Annotated[
            str,
            Form(
                title="Encoding",
                description="Text decoding method",
                examples=["utf-8"],
            ),
            BeforeValidator(SmartValueParser[str]().value_or_first_element),
        ] = "utf-8",
        hi_res_model_name: Annotated[
            Optional[str],
            Form(
                title="Hi-Res Model",
                description="Inference model for hi_res strategy",
                examples=["yolox"],
            ),
            BeforeValidator(SmartValueParser[str]().value_or_first_element),
        ] = None,
        include_page_breaks: Annotated[
            bool,
            Form(
                title="Include Page Breaks",
                description="Include page breaks where supported",
            ),
            BeforeValidator(SmartValueParser[str]().value_or_first_element),
        ] = False,
        pdf_infer_table_structure: Annotated[
            bool,
            Form(
                title="PDF Table Extraction",
                description="DEPRECATED: Use skip_infer_table_types instead",
            ),
            BeforeValidator(SmartValueParser[bool]().value_or_first_element),
        ] = True,
        strategy: Annotated[
            Literal["fast", "hi_res", "auto", "ocr_only"],
            Form(
                title="Partition Strategy",
                description="Strategy for PDF/image partitioning",
                examples=["auto", "hi_res"],
            ),
            BeforeValidator(SmartValueParser[str]().literal_value_stripped_or_first_element),
        ] = "auto",
        extract_image_block_types: Annotated[
            List[str],
            Form(
                title="Image Block Types",
                description="Element types to extract as base64",
                examples=["""["image", "table"]"""],
            ),
            BeforeValidator(SmartValueParser[List[str]]().value_or_first_element),
        ] = [],  # noqa
        unique_element_ids: Annotated[
            bool,
            Form(
                title="Unique Element IDs",
                description="Use UUIDs instead of SHA-256 for element IDs",
                examples=[True],
            ),
        ] = False,
        # Chunking options
        chunking_strategy: Annotated[
            Optional[
                Literal[
                    "by_title", "basic", "character", "recursive", "token",
                    "markdown", "python", "latex", "nltk", "spacy",
                    "html_header", "sentence_transformers", "language"
                ]
            ],
            Form(
                title="Chunking Strategy",
                description="Strategy for chunking elements",
                examples=["by_title"],
            ),
        ] = None,
        combine_under_n_chars: Annotated[
            Optional[int],
            Form(
                title="Combine Under N Chars",
                description="Combine elements until reaching length",
                examples=[500],
            ),
        ] = None,
        max_characters: Annotated[
            int,
            Form(
                title="Max Characters",
                description="Hard max length for new sections",
                examples=[1500],
            ),
        ] = 500,
        multipage_sections: Annotated[
            bool,
            Form(
                title="Multipage Sections",
                description="Allow sections to span multiple pages",
            ),
        ] = True,
        new_after_n_chars: Annotated[
            Optional[int],
            Form(
                title="New After N Chars",
                description="Soft max length for new sections",
                examples=[1500],
            ),
        ] = None,
        overlap: Annotated[
            int,
            Form(
                title="Overlap",
                description="Overlap length between chunks",
                examples=[20],
            ),
        ] = 0,
        overlap_all: Annotated[
            bool,
            Form(
                title="Overlap All",
                description="Apply overlap to all chunks (use with caution)",
                examples=[True],
            ),
        ] = False,
        starting_page_number: Annotated[
            Optional[int],
            Form(
                title="Starting Page Number",
                description="Initial page number for split PDFs",
                examples=[3],
            ),
        ] = None,
        include_slide_notes: Annotated[
            bool,
            Form(
                title="Include Slide Notes",
                description="Include PPT/PPTX slide notes in response",
                examples=[False],
            ),
        ] = True,
    ) -> "GeneralFormParams":
        """Construct form parameters from request data"""
        # Collect known parameters
        known_params = {
            "xml_keep_tags": xml_keep_tags,
            "languages": languages if languages else None,
            "ocr_languages": ocr_languages if ocr_languages else None,
            "skip_infer_table_types": skip_infer_table_types,
            "gz_uncompressed_content_type": gz_uncompressed_content_type,
            "output_format": output_format,
            "coordinates": coordinates,
            "content_type": content_type,
            "encoding": encoding,
            "hi_res_model_name": hi_res_model_name,
            "include_page_breaks": include_page_breaks,
            "pdf_infer_table_structure": pdf_infer_table_structure,
            "strategy": strategy,
            "extract_image_block_types": (
                extract_image_block_types if extract_image_block_types else None
            ),
            "chunking_strategy": chunking_strategy,
            "combine_under_n_chars": combine_under_n_chars,
            "max_characters": max_characters,
            "multipage_sections": multipage_sections,
            "new_after_n_chars": new_after_n_chars,
            "overlap": overlap,
            "overlap_all": overlap_all,
            "unique_element_ids": unique_element_ids,
            "starting_page_number": starting_page_number,
            "include_slide_notes": include_slide_notes
        }

        # Extract form data
        form_data = await request.form()
        dynamic_params = {}

        # Process dynamic parameters
        for key, value in form_data.items():
            # Skip known parameters and special keys
            if key in known_params or key in ["files", "__len__", "combine_text_under_n_chars"]:
                continue

            # Parse value using SmartValueParser
            dynamic_params[key] = value

        # Create instance with known parameters
        instance = cls(**known_params)

        # Add dynamic parameters
        instance.splitter_kwargs = dynamic_params

        return instance
