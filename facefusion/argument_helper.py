from facefusion.filesystem import get_file_name, is_video, resolve_file_paths
from facefusion.normalizer import normalize_fps, normalize_space
from facefusion.processors.core import get_processors_modules
from facefusion.types import ApplyStateItem, Arguments
from facefusion.vision import detect_video_fps


def apply_arguments(arguments : Arguments, apply_state_item : ApplyStateItem) -> None:
	# general
	apply_state_item('command', arguments.get('command'))
	# workflow
	apply_state_item('workflow', arguments.get('workflow'))
	# paths
	apply_state_item('temp_path', arguments.get('temp_path'))
	apply_state_item('jobs_path', arguments.get('jobs_path'))
	apply_state_item('source_paths', arguments.get('source_paths'))
	apply_state_item('target_path', arguments.get('target_path'))
	apply_state_item('output_path', arguments.get('output_path'))
	# patterns
	apply_state_item('source_pattern', arguments.get('source_pattern'))
	apply_state_item('target_pattern', arguments.get('target_pattern'))
	apply_state_item('output_pattern', arguments.get('output_pattern'))
	# face detector
	apply_state_item('face_detector_model', arguments.get('face_detector_model'))
	apply_state_item('face_detector_size', arguments.get('face_detector_size'))
	apply_state_item('face_detector_margin', normalize_space(arguments.get('face_detector_margin')))
	apply_state_item('face_detector_angles', arguments.get('face_detector_angles'))
	apply_state_item('face_detector_score', arguments.get('face_detector_score'))
	# face landmarker
	apply_state_item('face_landmarker_model', arguments.get('face_landmarker_model'))
	apply_state_item('face_landmarker_score', arguments.get('face_landmarker_score'))
	# face selector
	apply_state_item('face_selector_mode', arguments.get('face_selector_mode'))
	apply_state_item('face_selector_order', arguments.get('face_selector_order'))
	apply_state_item('face_selector_age_start', arguments.get('face_selector_age_start'))
	apply_state_item('face_selector_age_end', arguments.get('face_selector_age_end'))
	apply_state_item('face_selector_gender', arguments.get('face_selector_gender'))
	apply_state_item('face_selector_race', arguments.get('face_selector_race'))
	apply_state_item('reference_face_position', arguments.get('reference_face_position'))
	apply_state_item('reference_face_distance', arguments.get('reference_face_distance'))
	apply_state_item('reference_frame_number', arguments.get('reference_frame_number'))
	# face masker
	apply_state_item('face_occluder_model', arguments.get('face_occluder_model'))
	apply_state_item('face_parser_model', arguments.get('face_parser_model'))
	apply_state_item('face_mask_types', arguments.get('face_mask_types'))
	apply_state_item('face_mask_areas', arguments.get('face_mask_areas'))
	apply_state_item('face_mask_regions', arguments.get('face_mask_regions'))
	apply_state_item('face_mask_blur', arguments.get('face_mask_blur'))
	apply_state_item('face_mask_padding', normalize_space(arguments.get('face_mask_padding')))
	# voice extractor
	apply_state_item('voice_extractor_model', arguments.get('voice_extractor_model'))
	# frame extraction
	apply_state_item('trim_frame_start', arguments.get('trim_frame_start'))
	apply_state_item('trim_frame_end', arguments.get('trim_frame_end'))
	apply_state_item('temp_frame_format', arguments.get('temp_frame_format'))
	# output creation
	apply_state_item('output_image_quality', arguments.get('output_image_quality'))
	apply_state_item('output_image_scale', arguments.get('output_image_scale'))
	apply_state_item('output_audio_encoder', arguments.get('output_audio_encoder'))
	apply_state_item('output_audio_quality', arguments.get('output_audio_quality'))
	apply_state_item('output_audio_volume', arguments.get('output_audio_volume'))
	apply_state_item('output_video_encoder', arguments.get('output_video_encoder'))
	apply_state_item('output_video_preset', arguments.get('output_video_preset'))
	apply_state_item('output_video_quality', arguments.get('output_video_quality'))
	apply_state_item('output_video_scale', arguments.get('output_video_scale'))
	if arguments.get('output_video_fps') or is_video(arguments.get('target_path')):
		output_video_fps = normalize_fps(arguments.get('output_video_fps')) or detect_video_fps(arguments.get('target_path'))
		apply_state_item('output_video_fps', output_video_fps)
	# processors
	available_processors = [ get_file_name(file_path) for file_path in resolve_file_paths('facefusion/processors/modules') ]
	apply_state_item('processors', arguments.get('processors'))
	for processor_module in get_processors_modules(available_processors):
		processor_module.apply_arguments(arguments, apply_state_item)
	# execution
	apply_state_item('execution_device_ids', arguments.get('execution_device_ids'))
	apply_state_item('execution_providers', arguments.get('execution_providers'))
	apply_state_item('execution_thread_count', arguments.get('execution_thread_count'))
	# download
	apply_state_item('download_providers', arguments.get('download_providers'))
	apply_state_item('download_scope', arguments.get('download_scope'))
	# benchmark
	apply_state_item('benchmark_mode', arguments.get('benchmark_mode'))
	apply_state_item('benchmark_resolutions', arguments.get('benchmark_resolutions'))
	apply_state_item('benchmark_cycle_count', arguments.get('benchmark_cycle_count'))
	# api
	apply_state_item('api_host', arguments.get('api_host'))
	apply_state_item('api_port', arguments.get('api_port'))
	# memory
	apply_state_item('video_memory_strategy', arguments.get('video_memory_strategy'))
	# misc
	apply_state_item('log_level', arguments.get('log_level'))
	apply_state_item('halt_on_error', arguments.get('halt_on_error'))
	# jobs
	apply_state_item('job_id', arguments.get('job_id'))
	apply_state_item('job_status', arguments.get('job_status'))
	apply_state_item('step_index', arguments.get('step_index'))
