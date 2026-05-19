from django import forms


class ScoreSubmissionForm(forms.Form):
    comments = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 4}))

    def __init__(self, *args, rubric_items=None, is_draft=False, **kwargs):
        super().__init__(*args, **kwargs)
        rubric_items = rubric_items or []
        for item in rubric_items:
            choices = [(i, str(i)) for i in range(item.min_score, item.max_score + 1)]
            self.fields[f"item_{item.id}"] = forms.ChoiceField(
                choices=choices,
                widget=forms.RadioSelect,
                required=not is_draft,
                label=item.label,
                help_text=item.description,
            )


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()
